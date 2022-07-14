from abc import ABC, abstractmethod
from datetime import datetime

import pytz
from dateutil.parser import *


class ITellingTime:
    @abstractmethod
    def get_time(self) -> datetime:
        raise NotImplementedError()


class FakeClock(ITellingTime):
    def __init__(self, datetime_str: str):
        self._time = parse(datetime_str)

    def get_time(self):
        return self._time


class RealClock(ITellingTime):
    def get_time(self, timezone: str = ""):
        if timezone == "":
            return pytz.utc.localize(datetime.utcnow())
        utc = pytz.utc.localize(datetime.utcnow())
        return utc.astimezone(pytz.timezone(timezone))

    def convert_est_to_utc(self, est_datetime: datetime):
        local_tz = pytz.timezone("America/New_York")
        localdt = local_tz.localize(est_datetime)
        return localdt.astimezone(pytz.UTC)
