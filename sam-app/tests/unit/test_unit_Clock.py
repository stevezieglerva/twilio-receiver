import time
import unittest
from datetime import datetime
from unittest.mock import MagicMock, Mock, PropertyMock, patch

from Clock import FakeClock, RealClock
from pytz import UTC


class FakeClockUnitTests(unittest.TestCase):
    def test_should_get_fake_time(self):
        # Arrange
        subject = FakeClock("2022-01-01 09:00:01")

        # Act
        results = subject.get_time()
        print(f"test results: {results}")

        # Assert
        self.assertEqual(results, datetime(2022, 1, 1, 9, 0, 1, tzinfo=UTC))


class RealClockUnitTests(unittest.TestCase):
    def test_should_get_real_time(self):
        # Arrange
        subject = RealClock()

        # Act
        time_1 = subject.get_time()
        time.sleep(1)
        time_2 = subject.get_time()

        # Assert
        self.assertNotEqual(time_1, time_2)

    def test_should_get_est_time(self):
        # Arrange
        subject = RealClock()

        # Act
        time_1 = subject.get_time()
        print(f"time_1: {time_1}")
        time.sleep(1)
        time_2 = subject.get_time("America/New_York")
        print(f"time_2: {time_2}")

        # Assert
        self.assertTrue(time_1.hour != time_2.hour)
        self.assertTrue(time_1.tzname != time_2.tzname)

    def test_should_convert_est_to_utc(self):
        # Arrange
        subject = RealClock()

        # Act
        results = subject.convert_est_to_utc(datetime(2020, 1, 1, 13, 0, 0))

        # Assert
        self.assertTrue(results.hour >= 17)


if __name__ == "__main__":
    unittest.main()
