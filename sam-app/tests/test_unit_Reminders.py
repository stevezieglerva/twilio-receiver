import unittest
from unittest.mock import MagicMock, Mock, PropertyMock, patch

from common_layer.python.domain.Reminders import (
    Reminder,
    RemindersConfig,
    ReminderSender,
    ReminderStatuses,
)
from common_layer.python.infrastructure.repository.StorageRepo import FakeRepo
from common_layer.python.infrastructure.system.Clock import FakeClock


class RemindersUnitTests(unittest.TestCase):
    def test_should_send_text_if_time_right(self):
        # Arrange
        config = RemindersConfig()
        config.add_reminder(
            "Take medicine",
            ["09:00", "10:00"],
        )

        clock = FakeClock("2020-01-01 09:00:01")

        subject = ReminderSender(config, clock, FakeRepo())

        # Act
        results = subject.send_needed_reminder_texts()
        print(f"test results: {results}")

        # Assert
        self.assertEqual(results[0].name, "Take medicine")

    def test_should_send_not_text_if_time_wrong(self):
        # Arrange
        config = RemindersConfig()
        config.add_reminder(
            "Take medicine",
            ["09:00", "10:00"],
        )

        clock = FakeClock("2020-01-01 08:59:59")

        subject = ReminderSender(config, clock, FakeRepo())

        # Act
        results = subject.send_needed_reminder_texts()
        print(f"test results: {results}")

        # Assert
        self.assertEqual(len(results), 0)

    def test_should_activate_reminder_when_texted(self):
        # Arrange
        config = RemindersConfig()
        config.add_reminder(
            "Take medicine",
            ["09:00", "10:00"],
        )

        clock = FakeClock("2020-01-01 09:00:01")

        subject = ReminderSender(config, clock, FakeRepo())

        # Act
        results = subject.send_needed_reminder_texts()
        print(f"test results: {results}")

        # Assert
        self.assertEqual(results[0].status, ReminderStatuses.ACTIVE)
        self.assertTrue(results[0].last_sent is not None)
        self.assertEqual(results[0].occurences, 1)


if __name__ == "__main__":
    unittest.main()
