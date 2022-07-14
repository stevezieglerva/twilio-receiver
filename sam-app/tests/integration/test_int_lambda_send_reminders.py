import os
import unittest
from time import sleep
from unittest.mock import MagicMock, Mock, PropertyMock, patch

import boto3
from domain.ReminderSender import *
from infrastructure.repository.S3 import *
from infrastructure.repository.StorageRepo import *
from send_scheduled_reminders.app import *


class SendRemindersIntegrationTests(unittest.TestCase):
    def test_should_send_necessary_reminders(self):
        # Arrange
        bucket = "twilio-apps"
        os.environ["S3_BUCKET"] = bucket
        key_prefix = "test/integration"
        os.environ["S3_KEY_PREFIX"] = key_prefix
        s3 = S3()

        s3.delete_object(bucket, f"{key_prefix}/reminders.json")
        repo = S3Repo(bucket, key_prefix, s3)
        repo.save_reminder(
            Reminder(
                "integration lambda test - Take medicine", ["00:00"], ["+19193229617"]
            )
        )

        # Act
        # send several reminders to show the occurrences increase
        results = lambda_handler({}, "")
        sleep(5)
        results = lambda_handler({}, "")
        sleep(5)
        results = lambda_handler({}, "")
        sleep(5)
        results = lambda_handler({}, "")
        print(f"test results: {json.dumps(results, indent=3, default=str)}")

        # Assert
        self.assertEqual(
            results[0]["reminder"]["name"], "integration lambda test - Take medicine"
        )


if __name__ == "__main__":
    unittest.main()
