import unittest
from unittest.mock import MagicMock, Mock, PropertyMock, patch

from common_layer.python.domain.Reminders import (
    Reminder,
    RemindersConfig,
    ReminderSender,
)
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

        subject = ReminderSender(config, clock)

        # Act
        results = subject.send_needed_reminder_texts()
        print(f"test results: {results}")

        # Assert
        self.assertEqual(results[0].name, "Take medicine")


if __name__ == "__main__":
    unittest.main()
