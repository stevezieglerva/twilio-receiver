import unittest
from unittest.mock import MagicMock, Mock, PropertyMock, patch

import RemindersDTO


class ReminderConfigUnitTests(unittest.TestCase):
    def test_should_add_reminder(self):
        # Arrange
        subject = RemindersDTO.RemindersConfig()

        # Act
        results = subject.add_reminder("Take medicine", ["09:00", "10:00"])
        print(f"test results: {results}")

        # Assert
        reminders = subject.get_reminders()
        self.assertEqual(reminders[0].times, ["09:00", "10:00"])


if __name__ == "__main__":
    unittest.main()
