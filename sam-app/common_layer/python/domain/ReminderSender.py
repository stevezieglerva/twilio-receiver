from dataclasses import dataclass
from datetime import datetime
from typing import List

import StorageRepo
from common_layer.python.infrastructure.system.Clock import ITellingTime
from dateutil.parser import *


class ReminderSender:
    _config: RemindersConfig
    _clock: ITellingTime
    # _repo: IStoringReminders

    def __init__(
        self, config: RemindersConfig, clock: ITellingTime
    ):  # , repo: IStoringReminders

        self._config = config
        self._clock = clock
        # self._repo = repo

    def send_needed_reminder_texts(self) -> List[Reminder]:
        sent_reminders = []
        reminders = self._config.get_reminders()
        for reminder in reminders:
            if self._should_send_text(reminder):
                updated_reminder = Reminder(
                    name=reminder.name,
                    times=reminder.times,
                    status=ReminderStatuses.ACTIVE,
                    last_sent=self._clock.get_time(),
                    occurences=reminder.occurences + 1,
                )
                sent_reminders.append(updated_reminder)

        return sent_reminders

    def _should_send_text(self, reminder):
        now = self._clock.get_time()
        for reminder_time in reminder.times:
            reminder_time_str = f"{now.year}-{now.month}-{now.day} {reminder_time}"
            print(f"{reminder_time_str}")
            reminder_time_for_today = parse(reminder_time_str)
            print(f"{reminder_time_for_today}")
            print(reminder_time)
            if now >= reminder_time_for_today:
                return True
        return False
