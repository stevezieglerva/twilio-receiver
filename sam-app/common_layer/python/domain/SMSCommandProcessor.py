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
        print(f"Processing command: {command}")
        if command.body.lower() == SMSCommands.DONE:
            active_reminder = self._s3_repo.get_active_reminder()
            print(f"Found active reminder: {active_reminder}")
            done_reminder = Reminder(
                name=active_reminder.name,
                times=active_reminder.times,
                phone_numbers=active_reminder.phone_numbers,
                status=ReminderStatuses.DONE,
                last_sent=active_reminder.last_sent,
                occurences=0,
                last_set_to_done=self._clock.get_time().isoformat(),
            )
            self._s3_repo.save_reminder(done_reminder)
            update_message = f"✅ '{done_reminder.name}' marked as done by {command.from_phone_number}."
            for phone_number in done_reminder.phone_numbers:
                self._twilio_client.send_text(phone_number, update_message)

            return SMSCommandResult(
                timestamp=self._clock.get_time().isoformat(),
                command=command,
                result="ok",
                result_details=update_message,
            )

        unknown_command_msg = f"⁉️ '{command.body}' is an unknown commmand."
        self._twilio_client.send_text(command.from_phone_number, unknown_command_msg)

        return SMSCommandResult(
            timestamp=self._clock.get_time().isoformat(),
            command=command,
            result="error",
            result_details=unknown_command_msg,
        )
