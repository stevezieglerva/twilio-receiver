import os
import unittest
from datetime import datetime
from unittest.mock import MagicMock, Mock, PropertyMock, patch

from infrastructure.notifications.Twilio import *


class TwilioUnitTests(unittest.TestCase):
    def test_should_send_text(self):
        # Arrange
        subject = FakeTwilio("abc", "123")

        # Act
        results = subject.send_text(
            "+11234567890", f"Here's a test message at {datetime.now()}"
        )
        print(f"test results: {results}")

        # Assert
        self.assertTrue(results.date != "")


if __name__ == "__main__":
    unittest.main()
