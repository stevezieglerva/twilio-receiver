import unittest
from unittest.mock import MagicMock, Mock, PropertyMock, patch

from common_layer.python.domain.Reminders import Reminder, ReminderStatuses
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

    def test_should_store_reminder_to_update_one_reminder(self):
        # Arrange
        subject = FakeRepo()
        subject.store_reminder(Reminder("Take medicine", ["09:00", "10:00"]))
        subject.store_reminder(Reminder("Take medicine 2", ["12:00", "13:00"]))
        subject.store_reminder(Reminder("Take medicine 3", ["15:00", "16:00"]))

        # Act
        subject.store_reminder(
            Reminder(
                name="Take medicine 2",
                times=["12:00", "13:00"],
                status=ReminderStatuses.ACTIVE,
            )
        )

        # Assert
        reminder = subject.get_reminder("Take medicine 2")
        self.assertEqual(reminder.times, ["12:00", "13:00"])
        self.assertEqual(reminder.status, ReminderStatuses.ACTIVE)


if __name__ == "__main__":
    unittest.main()
