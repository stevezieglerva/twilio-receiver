from abc import ABC, abstractmethod
from datetime import datetime

from dateutil.parser import *


class ITellingTime:
    @abstractmethod
    def get_time(self) -> datetime:
        pass


class FakeClock(ITellingTime):
    def __init__(self, datetime_str: str):
        self._time = parse(datetime_str)

    def get_time(self):
        return self._time


class RealClock(ITellingTime):
    def get_time(self):
        return datetime.now()
