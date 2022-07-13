import unittest
from unittest.mock import MagicMock, Mock, PropertyMock, patch

import Clock
import RemindersDTO
import ReminderSender
import StorageRepo
from TwilioClient import *


class RemindersUnitTests(unittest.TestCase):
    def test_should_send_text_if_time_right(self):
        # Arrange

        clock = Clock.FakeClock("2020-01-01 09:00:01")
        repo = StorageRepo.FakeRepo()
        repo.save_reminder(RemindersDTO.Reminder("Take medicine", ["09:00", "10:00"]))
        twilio = FakeTwilio("abc", "123")
        subject = ReminderSender.ReminderSender(clock, repo, twilio)

        # Act
        results = subject.send_needed_reminder_texts()
        print(f"test results: {results}")

        # Assert
        self.assertEqual(results[0].name, "Take medicine")

    def test_should_send_not_text_if_time_wrong(self):
        # Arrange

        clock = Clock.FakeClock("2020-01-01 08:59:59")
        repo = StorageRepo.FakeRepo()
        repo.save_reminder(RemindersDTO.Reminder("Take medicine", ["09:00", "10:00"]))
        twilio = FakeTwilio("abc", "123")
        subject = ReminderSender.ReminderSender(clock, repo, twilio)

        # Act
        results = subject.send_needed_reminder_texts()
        print(f"test results: {results}")

        # Assert
        self.assertEqual(len(results), 0)

    def test_should_activate_reminder_when_texted(self):
        # Arrange

        clock = Clock.FakeClock("2020-01-01 09:00:01")
        repo = StorageRepo.FakeRepo()
        repo.save_reminder(RemindersDTO.Reminder("Take medicine", ["09:00", "10:00"]))
        twilio = FakeTwilio("abc", "123")
        subject = ReminderSender.ReminderSender(clock, repo, twilio)

        # Act
        results = subject.send_needed_reminder_texts()
        print(f"test results: {results}")

        # Assert
        self.assertEqual(results[0].status, RemindersDTO.ReminderStatuses.ACTIVE)
        self.assertTrue(results[0].last_sent is not None)
        self.assertEqual(results[0].occurences, 1)

    def test_should_save_activated_reminder_in_repo(self):
        # Arrange

        clock = Clock.FakeClock("2020-01-01 09:00:01")
        repo = StorageRepo.FakeRepo()
        repo.save_reminder(RemindersDTO.Reminder("Take medicine", ["09:00", "10:00"]))
        twilio = FakeTwilio("abc", "123")
        subject = ReminderSender.ReminderSender(clock, repo, twilio)

        # Act
        results = subject.send_needed_reminder_texts()
        print(f"test results: {results}")

        # Assert
        saved_reminder = repo.get_reminder("Take medicine")
        self.assertEqual(saved_reminder.status, RemindersDTO.ReminderStatuses.ACTIVE)

    def test_should_not_send_if_reminder_is_done(self):
        # Arrange

        clock = Clock.FakeClock("2020-01-01 09:00:01")
        repo = StorageRepo.FakeRepo()
        repo.save_reminder(
            RemindersDTO.Reminder(
                "Take medicine",
                ["09:00", "10:00"],
                status=RemindersDTO.ReminderStatuses.DONE,
            )
        )
        twilio = FakeTwilio("abc", "123")
        subject = ReminderSender.ReminderSender(clock, repo, twilio)

        # Act
        results = subject.send_needed_reminder_texts()
        print(f"test results: {results}")

        # Assert
        self.assertEqual(results, [])


if __name__ == "__main__":
    unittest.main()
