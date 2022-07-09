from dataclasses import dataclass
from datetime import datetime
from typing import List

from common_layer.python.infrastructure.system.Clock import ITellingTime
from dateutil.parser import *


@dataclass(frozen=True)
class Reminder:
    name: str
    times: List[str]
    status: str = ""
    last_sent: datetime = None
    occurences: int = 0


class RemindersConfig:
    _reminders = []

    def add_reminder(self, name: str, times: List[str]) -> None:
        self._reminders.append(Reminder(name=name, times=times))

    def get_reminders(self) -> List[Reminder]:
        return self._reminders


class ReminderSender:
    _config: RemindersConfig
    _clock: ITellingTime

    def __init__(self, config: RemindersConfig, clock: ITellingTime):
        self._config = config
        self._clock = clock

    def send_needed_reminder_texts(self) -> List[Reminder]:
        sent_reminders = []
        reminders = self._config.get_reminders()
        for reminder in reminders:
            if self._should_send_text(reminder):
                sent_reminders.append(reminder)

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
