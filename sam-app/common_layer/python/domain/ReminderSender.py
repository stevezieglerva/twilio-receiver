from dataclasses import dataclass
from datetime import datetime
from typing import List

import Clock
import StorageRepo
from dateutil.parser import *

import RemindersDTO


class ReminderSender:
    _config: RemindersDTO.RemindersConfig
    _clock: Clock.ITellingTime
    _repo: StorageRepo.IStoringReminders

    def __init__(
        self,
        config: RemindersDTO.RemindersConfig,
        clock: Clock.ITellingTime,
        repo: StorageRepo.IStoringReminders,
    ):

        self._config = config
        self._clock = clock
        self._repo = repo

    def send_needed_reminder_texts(self) -> List[RemindersDTO.Reminder]:
        sent_reminders = []
        reminders = self._repo.get_reminders()
        for reminder in reminders:
            print(f"Checking '{reminder.name}'")
            if self._should_send_text(reminder):
                updated_reminder = RemindersDTO.Reminder(
                    name=reminder.name,
                    times=reminder.times,
                    status=RemindersDTO.ReminderStatuses.ACTIVE,
                    last_sent=self._clock.get_time(),
                    occurences=reminder.occurences + 1,
                )
                print(f"\tSending reminder for '{updated_reminder.name}'")
                self._repo.save_reminder(updated_reminder)
                sent_reminders.append(updated_reminder)

        return sent_reminders

    def _should_send_text(self, reminder):
        now = self._clock.get_time()
        for reminder_time in reminder.times:
            reminder_time_str = f"{now.year}-{now.month}-{now.day} {reminder_time}"
            reminder_time_for_today = parse(reminder_time_str)
            print(
                f"\tAt {self._clock.get_time()}, reminder is {reminder.status} for {reminder_time_for_today}"
            )
            if reminder.status == RemindersDTO.ReminderStatuses.DONE:
                print(f"\tReminder is done. Skipping")
                return False
            if now >= reminder_time_for_today:
                return True
        return False
