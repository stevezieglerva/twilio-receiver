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
    phone_numbers: List[str]
    status: str = ReminderStatuses.INACTIVE
    last_sent: str = ""
    occurences: int = 0


class DuplicateReminderNameException(ValueError):
    pass
