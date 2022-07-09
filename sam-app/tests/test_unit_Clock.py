import unittest
from datetime import datetime
from unittest.mock import MagicMock, Mock, PropertyMock, patch

from common_layer.python.infrastructure.system.Clock import FakeClock


class FakeClockUnitTests(unittest.TestCase):
    def test_should_get_fake_time(self):
        # Arrange
        subject = FakeClock("2022-01-01 09:00:01")

        # Act
        results = subject.get_time()
        print(f"test results: {results}")

        # Assert
        self.assertEqual(results, datetime(2022, 1, 1, 9, 0, 1))


if __name__ == "__main__":
    unittest.main()
