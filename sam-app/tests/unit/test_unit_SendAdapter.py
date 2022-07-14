import unittest
from unittest.mock import MagicMock, Mock, PropertyMock, patch

import Clock
import RemindersDTO
import ReminderSender
import SendAdapter
import StorageRepo
from infrastructure.notifications.TwilioClient import FakeTwilio


class SendAdapterUnitTests(unittest.TestCase):
    def test_should_send_notifications_on_cron_event(self):
        # Arrange
        clock = Clock.FakeClock("2020-01-01 10:00:01")
        repo = StorageRepo.FakeRepo()
        repo.save_reminder(RemindersDTO.Reminder("Take medicine", ["05:00"], ["333"]))
        twilio = FakeTwilio("abc", "123")
        reminder_sender = ReminderSender.ReminderSender(clock, repo, twilio)

        subject = SendAdapter.SendAdapter(reminder_sender)

        # Act
        results = subject.send_reminders()
        print(f"test results: {results}")

        # Assert
        self.assertEqual(results[0].reminder.name, "Take medicine")


if __name__ == "__main__":
    unittest.main()
