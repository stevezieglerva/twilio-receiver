from dataclasses import dataclass
from datetime import datetime
from typing import List

import pytz
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
        for count, reminder in enumerate(reminders):
            print(f"\nChecking #{count+1}: '{reminder}'")

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
        date_display = self._clock.get_time("America/New_York").strftime(
            "%m/%d/%Y %H:%M:%S"
        )
        reminder_occurrence = ""
        if reminder.occurences > 1:
            reminder_occurrence = f"#{reminder.occurences + 1}"
        text_message = f"""
⏰ Reminder {reminder_occurrence}
{reminder.name}
Sent: {date_display}
Text 'done' to mark as done.
"""

        return text_message

    def _should_send_text(self, reminder):
        now = self._clock.get_time()
        for count, reminder_time in enumerate(reminder.times):
            print(f"\n\tChecking time #{count+1}: '{reminder_time}'")
            reminder_time_str = f"{now.year}-{now.month}-{now.day} {reminder_time}"
            reminder_time_for_today = parse(reminder_time_str)
            utc_reminder_for_today = self._clock.convert_est_to_utc(
                reminder_time_for_today
            )

            print(
                f"\tAt {now}, reminder is {reminder.status} scheduled for {utc_reminder_for_today} "
            )
            if reminder.last_set_to_done != "":
                last_set_to_done = parse(reminder.last_set_to_done)
                if (
                    reminder.status == ReminderStatuses.DONE
                    and utc_reminder_for_today < last_set_to_done
                ):
                    print(f"\tReminder is done. Skipping")
                    continue

            print(
                f"""\tComparing 
\t{utc_reminder_for_today} alarm to 
\t{now} now"""
            )
            if now >= utc_reminder_for_today:
                print(f"\t\tReminder is due based on time.")
                return True
        return False
