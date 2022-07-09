import unittest
from unittest.mock import MagicMock, Mock, PropertyMock, patch

import Clock
import RemindersDTO
import ReminderSender
import StorageRepo


class RemindersUnitTests(unittest.TestCase):
    def test_should_send_text_if_time_right(self):
        # Arrange
        config = RemindersDTO.RemindersConfig()
        config.add_reminder(
            "Take medicine",
            ["09:00", "10:00"],
        )

        clock = Clock.FakeClock("2020-01-01 09:00:01")

        subject = ReminderSender.ReminderSender(config, clock, StorageRepo.FakeRepo())

        # Act
        results = subject.send_needed_reminder_texts()
        print(f"test results: {results}")

        # Assert
        self.assertEqual(results[0].name, "Take medicine")

    def test_should_send_not_text_if_time_wrong(self):
        # Arrange
        config = RemindersDTO.RemindersConfig()
        config.add_reminder(
            "Take medicine",
            ["09:00", "10:00"],
        )

        clock = Clock.FakeClock("2020-01-01 08:59:59")

        subject = ReminderSender.ReminderSender(config, clock, StorageRepo.FakeRepo())

        # Act
        results = subject.send_needed_reminder_texts()
        print(f"test results: {results}")

        # Assert
        self.assertEqual(len(results), 0)

    def test_should_activate_reminder_when_texted(self):
        # Arrange
        config = RemindersDTO.RemindersConfig()
        config.add_reminder(
            "Take medicine",
            ["09:00", "10:00"],
        )

        clock = Clock.FakeClock("2020-01-01 09:00:01")

        subject = ReminderSender.ReminderSender(config, clock, StorageRepo.FakeRepo())

        # Act
        results = subject.send_needed_reminder_texts()
        print(f"test results: {results}")

        # Assert
        self.assertEqual(results[0].status, RemindersDTO.ReminderStatuses.ACTIVE)
        self.assertTrue(results[0].last_sent is not None)
        self.assertEqual(results[0].occurences, 1)

    def test_should_save_activated_reminder_in_repo(self):
        # Arrange
        config = RemindersDTO.RemindersConfig()
        config.add_reminder(
            "Take medicine",
            ["09:00", "10:00"],
        )

        clock = Clock.FakeClock("2020-01-01 09:00:01")
        repo = StorageRepo.FakeRepo()
        subject = ReminderSender.ReminderSender(config, clock, repo)

        # Act
        results = subject.send_needed_reminder_texts()
        print(f"test results: {results}")

        # Assert
        saved_reminder = repo.get_reminder("Take medicine")
        self.assertEqual(saved_reminder.status, RemindersDTO.ReminderStatuses.ACTIVE)


if __name__ == "__main__":
    unittest.main()
