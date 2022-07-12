import os
import unittest
from datetime import datetime
from unittest.mock import MagicMock, Mock, PropertyMock, patch

from infrastructure.notifications.TwilioClient import *


class TwilioUnitTests(unittest.TestCase):
    def test_should_send_text(self):
        # Arrange
        account_sid = os.environ["TWILIO_ACCOUNT_SID"]
        auth_token = os.environ["TWILIO_AUTH_TOKEN"]
        subject = Twilio(account_sid, auth_token)

        # Act
        results = subject.send_text(
            "+19193229617", f"Here's a test message at {datetime.now()}"
        )
        print(f"test results: {results}")

        # Assert
        self.assertTrue(results.confirmation != "")


if __name__ == "__main__":
    unittest.main()
