import json
import unittest
from dataclasses import asdict, dataclass
from unittest.mock import MagicMock, Mock, PropertyMock, patch

import RemindersDTO
import S3
import StorageRepo

# class FakeRepoUnitTests(unittest.TestCase):
#     def test_should_store_reminder(self):
#         # Arrange
#         subject = StorageRepo.FakeRepo()

#         # Act
#         subject.save_reminder(
#             RemindersDTO.Reminder("Take medicine", ["09:00", "10:00"])
#         )

#         # Assert
#         reminder = subject.get_reminder("Take medicine")
#         self.assertEqual(reminder.times, ["09:00", "10:00"])

#     def test_should_store_reminder_to_update_one_reminder(self):
#         # Arrange
#         subject = StorageRepo.FakeRepo()
#         subject.save_reminder(
#             RemindersDTO.Reminder("Take medicine", ["09:00", "10:00"])
#         )
#         subject.save_reminder(
#             RemindersDTO.Reminder("Take medicine 2", ["12:00", "13:00"])
#         )
#         subject.save_reminder(
#             RemindersDTO.Reminder("Take medicine 3", ["15:00", "16:00"])
#         )

#         # Act
#         subject.save_reminder(
#             RemindersDTO.Reminder(
#                 name="Take medicine 2",
#                 times=["12:00", "13:00"],
#                 status=RemindersDTO.ReminderStatuses.ACTIVE,
#             )
#         )

#         # Assert
#         reminder = subject.get_reminder("Take medicine 2")
#         self.assertEqual(reminder.times, ["12:00", "13:00"])
#         self.assertEqual(reminder.status, RemindersDTO.ReminderStatuses.ACTIVE)


class S3RepoUnitTests(unittest.TestCase):
    def test_should_get_all_data(self):
        # Arrange
        s3 = S3.S3FakeLocal()
        subject = StorageRepo.S3Repo("fake--bucket", "testing__", s3)

        data = StorageRepo.RemindersDB(
            reminders=[RemindersDTO.Reminder("Take medicine", ["09:00", "10:00"])]
        )
        print(asdict(data))
        s3.put_object(
            "fake--bucket",
            "testing/reminders_db.json",
            json.dumps(asdict(data), indent=3, default=str),
        )

        # Act
        results = subject.get_all_data()

        # Assert
        self.assertEqual(results.reminders[0].name, "Take medicine")


if __name__ == "__main__":
    unittest.main()
