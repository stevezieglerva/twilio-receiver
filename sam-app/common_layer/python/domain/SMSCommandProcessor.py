from dataclasses import asdict, dataclass
from typing import List

from infrastructure.notifications.TwilioClient import *
from infrastructure.repository.StorageRepo import *
from infrastructure.system.Clock import *

from domain.SMSCommandDTO import *


@dataclass(frozen=True)
class SMSCommandResult:
    timestamp: str
    command: SMSCommand
    result: str
    result_details: str = ""


class SMSCommandProcessor:
    def __init__(
        self,
        s3_repo: IStoringReminders,
        clock: ITellingTime,
        twilio_client: IProcessingTexts,
    ):
        self._s3_repo = s3_repo
        self._clock = clock
        self._twilio_client = twilio_client

    def process_command(self, command: SMSCommand) -> SMSCommandResult:
        if command.body == SMSCommands.DONE:
            active_reminder = self._s3_repo.get_active_reminder()
            inactivated_reminder = Reminder(
                name=active_reminder.name,
                times=active_reminder.times,
                phone_numbers=active_reminder.phone_numbers,
                status=ReminderStatuses.INACTIVE,
                last_sent=active_reminder.last_sent,
                occurences=0,
            )
            self._s3_repo.save_reminder(inactivated_reminder)
            update_message = f"'{inactivated_reminder.name}' marked as done by {command.from_phone_number}."
            for phone_number in inactivated_reminder.phone_numbers:
                self._twilio_client.send_text(phone_number, update_message)

            return SMSCommandResult(
                timestamp=self._clock.get_time().isoformat(),
                command=command,
                result="ok",
                result_details=update_message,
            )

        return SMSCommandResult(
            timestamp=self._clock.get_time().isoformat(),
            command=command,
            result="error",
            result_details=f"'{command.body}' is an unknown commmand.",
        )
