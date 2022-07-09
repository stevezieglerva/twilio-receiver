import unittest
from unittest.mock import MagicMock, Mock, PropertyMock, patch


class RemindersUnitTests(unittest.TestCase):
    def test_should_send_text_if_time_right(self):
        # Arrange
        config = ReminderConfig()
        config.add_reminder(Reminder(["09:00", "10:00"], "Hello World"))
        subject = Reminders()

        # Act
        results = subject.send_needed_reminder_texts()
        print(f"test results: {results}")

        # Assert
        self.assertEqual(results, "")


if __name__ == "__main__":
    unittest.main()
