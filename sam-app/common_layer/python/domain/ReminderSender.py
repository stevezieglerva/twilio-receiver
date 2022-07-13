from dataclasses import dataclass
from datetime import datetime
from typing import List

from dateutil.parser import *
from infrastructure.notifications.TwilioClient import *
from infrastructure.repository.StorageRepo import *
from infrastructure.system.Clock import *

from domain.RemindersDTO import *


@dataclass(frozen=True)
class SentReminderText:
    reminder: Reminder
    sms_texts: List[SMSText]


class TwilioTextFailed(Exception):
    pass


class ReminderSender:
    _clock: ITellingTime
    _repo: IStoringReminders
    _twilio: IProcessingTexts

    def __init__(
        self,
        clock: ITellingTime,
        repo: IStoringReminders,
        twilio: IProcessingTexts,
    ):

        self._clock = clock
        self._repo = repo
        self._twilio = twilio

    def send_needed_reminder_texts(self) -> List[SentReminderText]:
        sent_reminders = []
        reminders = self._repo.get_reminders()
        for reminder in reminders:
            print(f"\nChecking '{reminder}'")

            if self._should_send_text(reminder):
                print("Attempting to send text.")
                text_message = self._create_reminder_text(reminder)
                updated_reminder = Reminder(
                    name=reminder.name,
                    times=reminder.times,
                    phone_numbers=reminder.phone_numbers,
                    status=ReminderStatuses.ACTIVE,
                    last_sent=self._clock.get_time().isoformat(),
                    occurences=reminder.occurences + 1,
                )

                sms_text_list = []
                for phone_number in reminder.phone_numbers:
                    twilio_response = self._twilio.send_text(phone_number, text_message)
                    print(f"Text sent to: {phone_number}")
                    print(f"{text_message}")
                    if twilio_response.confirmation == "":
                        raise TwilioTextFailed(
                            f"Couldn't send text to {twilio_response.phone_number} for the reminder '{reminder.name}'"
                        )
                    sms_text_list.append(twilio_response)

                sms_reminder_result = SentReminderText(updated_reminder, sms_text_list)
                sent_reminders.append(sms_reminder_result)

                print(f"\tUpdating DB for '{updated_reminder}'")
                self._repo.save_reminder(updated_reminder)
        return sent_reminders

    def _create_reminder_text(self, reminder):
        reminder_occurrence = ""
        if reminder.occurences > 1:
            reminder_occurrence = f"#{reminder.occurences + 1}"
        text_message = f"""
⏰ Reminder {reminder_occurrence}
{reminder.name}
Sent: {datetime.now().isoformat()}
Text 'done' to mark as done.
"""

        return text_message

    def _should_send_text(self, reminder):
        now = self._clock.get_time()
        for reminder_time in reminder.times:
            reminder_time_str = f"{now.year}-{now.month}-{now.day} {reminder_time}"
            reminder_time_for_today = parse(reminder_time_str)
            print(
                f"\tAt {self._clock.get_time()}, reminder is {reminder.status} for {reminder_time_for_today}"
            )
            if reminder.status == ReminderStatuses.DONE:
                print(f"\tReminder is done. Skipping")
                return False
            if now >= reminder_time_for_today:
                return True
        return False
