import json
import unittest
from dataclasses import asdict, dataclass
from datetime import datetime
from unittest.mock import MagicMock, Mock, PropertyMock, patch

import RemindersDTO
import S3
import StorageRepo


class S3RepoUnitTests(unittest.TestCase):
    def test_should_get_all_data(self):
        # Arrange
        s3 = S3.S3FakeLocal()
        subject = StorageRepo.S3Repo("fake--bucket", "unit_testing", s3)

        # Act
        results = subject.get_all_data()

        # Assert
        self.assertTrue(type(results) == StorageRepo.RemindersDB)

    def test_should_save_reminder(self):
        # Arrange
        s3 = S3.S3FakeLocal()
        subject = StorageRepo.S3Repo("fake--bucket", "unit_testing_b", s3)

        # Act
        subject.save_reminder(
            RemindersDTO.Reminder(
                "Take medicine", ["09:00", "10:00"], ["+1111111111", "+12222222222"]
            )
        )

        # Assert
        reminder = subject.get_reminder("Take medicine")
        self.assertEqual(reminder.times, ["09:00", "10:00"])

    def test_should_save_reminder_to_update_one_reminder(self):
        # Arrange
        s3 = S3.S3FakeLocal()
        subject = StorageRepo.S3Repo("fake--bucket", "unit_testing_c", s3)

        subject.save_reminder(
            RemindersDTO.Reminder(
                "Take medicine", ["09:00", "10:00"], ["+1111111111", "+12222222222"]
            )
        )
        subject.save_reminder(
            RemindersDTO.Reminder(
                "Take medicine 2", ["12:00", "13:00"], ["+1111111111", "+12222222222"]
            )
        )
        subject.save_reminder(
            RemindersDTO.Reminder(
                "Take medicine 3", ["15:00", "16:00"], ["+1111111111", "+12222222222"]
            )
        )

        # Act
        subject.save_reminder(
            RemindersDTO.Reminder(
                name="Take medicine 2",
                times=["12:00", "13:00"],
                phone_numbers=["+1111111111", "+12222222222"],
                status=RemindersDTO.ReminderStatuses.ACTIVE,
            )
        )

        # Assert
        reminder = subject.get_reminder("Take medicine 2")
        self.assertEqual(reminder.times, ["12:00", "13:00"])
        self.assertEqual(reminder.status, RemindersDTO.ReminderStatuses.ACTIVE)


if __name__ == "__main__":
    unittest.main()
