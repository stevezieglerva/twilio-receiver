from dataclasses import dataclass
from datetime import datetime
from typing import List

from dateutil.parser import *
from infrastructure.system import *


@dataclass(frozen=True)
class ReminderStatuses:
    INACTIVE: str = "inactive"
    ACTIVE: str = "active"
    DONE: str = "done"


@dataclass(frozen=True)
class Reminder:
    name: str
    times: List[str]
    status: str = ReminderStatuses.INACTIVE
    last_sent: str = ""
    occurences: int = 0


class DuplicateReminderNameException(ValueError):
    pass


class RemindersConfig:
    def __init__(self):
        self._reminders = []

    def add_reminder(self, name: str, times: List[str]) -> None:
        existing_names = [r.name for r in self._reminders]
        if name in existing_names:
            raise DuplicateReminderNameException(
                f"Reminder with name '{name}' already exists"
            )
        self._reminders.append(Reminder(name=name, times=times))

    def get_reminders(self) -> List[Reminder]:
        return self._reminders
