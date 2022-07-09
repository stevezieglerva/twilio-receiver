import unittest
from unittest.mock import MagicMock, Mock, PropertyMock, patch

from common_layer.python.domain.Reminders import Reminder
from common_layer.python.infrastructure.repository.StorageRepo import FakeRepo


class FakeRepoUnitTests(unittest.TestCase):
    def test_should_store_reminder(self):
        # Arrange
        subject = FakeRepo()

        # Act
        subject.store_reminder(Reminder("Take medicine", ["09:00", "10:00"]))

        # Assert
        reminder = subject.get_reminder("Take medicine")
        self.assertEqual(reminder.times, ["09:00", "10:00"])


if __name__ == "__main__":
    unittest.main()
