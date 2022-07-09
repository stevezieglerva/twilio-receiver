from dataclasses import dataclass
from datetime import datetime
from typing import List

from common_layer.python.infrastructure.system.Clock import ITellingTime
from dateutil.parser import *


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
    last_sent: datetime = None
    occurences: int = 0


class RemindersConfig:
    _reminders = []

    def add_reminder(self, name: str, times: List[str]) -> None:
        self._reminders.append(Reminder(name=name, times=times))

    def get_reminders(self) -> List[Reminder]:
        return self._reminders
