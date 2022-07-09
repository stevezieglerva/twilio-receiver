import unittest
from unittest.mock import MagicMock, Mock, PropertyMock, patch

import RemindersDTO
import StorageRepo


class FakeRepoUnitTests(unittest.TestCase):
    def test_should_store_reminder(self):
        # Arrange
        subject = StorageRepo.FakeRepo()

        # Act
        subject.store_reminder(
            RemindersDTO.Reminder("Take medicine", ["09:00", "10:00"])
        )

        # Assert
        reminder = subject.get_reminder("Take medicine")
        self.assertEqual(reminder.times, ["09:00", "10:00"])

    def test_should_store_reminder_to_update_one_reminder(self):
        # Arrange
        subject = StorageRepo.FakeRepo()
        subject.store_reminder(
            RemindersDTO.Reminder("Take medicine", ["09:00", "10:00"])
        )
        subject.store_reminder(
            RemindersDTO.Reminder("Take medicine 2", ["12:00", "13:00"])
        )
        subject.store_reminder(
            RemindersDTO.Reminder("Take medicine 3", ["15:00", "16:00"])
        )

        # Act
        subject.store_reminder(
            RemindersDTO.Reminder(
                name="Take medicine 2",
                times=["12:00", "13:00"],
                status=RemindersDTO.ReminderStatuses.ACTIVE,
            )
        )

        # Assert
        reminder = subject.get_reminder("Take medicine 2")
        self.assertEqual(reminder.times, ["12:00", "13:00"])
        self.assertEqual(reminder.status, RemindersDTO.ReminderStatuses.ACTIVE)


if __name__ == "__main__":
    unittest.main()
