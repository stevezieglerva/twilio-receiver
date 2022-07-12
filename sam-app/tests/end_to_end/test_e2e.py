import os
import unittest
from unittest.mock import MagicMock, Mock, PropertyMock, patch

import boto3
from domain.ReminderSender import *
from infrastructure.repository.S3 import *
from infrastructure.repository.StorageRepo import *


class EndToEndTests(unittest.TestCase):
    def test_should_send_necessary_reminders(self):
        # Arrange
        bucket = "twilio-apps"
        os.environ["S3_BUCKET"] = bucket
        key_prefix = "test"
        os.environ["S3_KEY_PREFIX"] = key_prefix
        s3 = S3()
        repo = S3Repo(bucket, key_prefix, s3)

        # Act
        results = subject.method()
        print(f"test results: {results}")

        # Assert
        self.assertEqual(results, "")


if __name__ == "__main__":
    unittest.main()
