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
