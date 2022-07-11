import unittest
from unittest.mock import MagicMock, Mock, PropertyMock, patch

import Clock
import RemindersDTO
import ReminderSender
import SendAdapter
import StorageRepo


class SendAdapterUnitTests(unittest.TestCase):
    def test_should_send_notifications_on_cron_event(self):
        # Arrange
        config = RemindersDTO.RemindersConfig()
        config.add_reminder(
            "Take medicine",
            ["09:00", "10:00"],
        )

        clock = Clock.FakeClock("2020-01-01 09:00:01")
        repo = StorageRepo.FakeRepo()
        repo.save_reminder(RemindersDTO.Reminder("Take medicine", ["09:00", "10:00"]))
        reminder_sender = ReminderSender.ReminderSender(config, clock, repo)

        subject = SendAdapter.SendAdapter(reminder_sender)

        # Act
        results = subject.send_reminders()
        print(f"test results: {results}")

        # Assert
        self.assertEqual(results[0].name, "Take medicine")


if __name__ == "__main__":
    unittest.main()
