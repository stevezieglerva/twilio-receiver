import time
import unittest
from datetime import datetime
from unittest.mock import MagicMock, Mock, PropertyMock, patch

from Clock import FakeClock, RealClock


class FakeClockUnitTests(unittest.TestCase):
    def test_should_get_fake_time(self):
        # Arrange
        subject = FakeClock("2022-01-01 09:00:01")

        # Act
        results = subject.get_time()
        print(f"test results: {results}")

        # Assert
        self.assertEqual(results, datetime(2022, 1, 1, 9, 0, 1))


class RealClockUnitTests(unittest.TestCase):
    def test_should_get_fake_time(self):
        # Arrange
        subject = RealClock()

        # Act
        time_1 = subject.get_time()
        time.sleep(1)
        time_2 = subject.get_time()

        # Assert
        self.assertNotEqual(time_1, time_2)


if __name__ == "__main__":
    unittest.main()
