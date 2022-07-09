from dataclasses import dataclass
from datetime import datetime
from typing import List


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

    def __init__(self, config: RemindersConfig):
        self._config = config

    def send_needed_reminder_texts(self) -> str:
        reminders = self._config.get_reminders()
        for reminder in reminders:
            if self._should_send_text(reminder):
                return reminder.name
        return ""
