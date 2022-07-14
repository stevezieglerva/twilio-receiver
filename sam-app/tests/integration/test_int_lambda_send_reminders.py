import os
import unittest
from datetime import datetime, timedelta
from time import sleep
from unittest.mock import MagicMock, Mock, PropertyMock, patch

import boto3
from domain.ReminderSender import *
from infrastructure.repository.S3 import *
from infrastructure.repository.StorageRepo import *
from send_scheduled_reminders.app import *


class SendRemindersIntegrationTests(unittest.TestCase):
    def test_should_send_necessary_reminders_with_increased_occurrences(self):
        # Arrange
        bucket = "twilio-apps"
        os.environ["S3_BUCKET"] = bucket
        key_prefix = "test/integation"
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
        results = lambda_handler({"s3_key_prefix": "test/integration"}, "")
        sleep(5)
        results = lambda_handler({"s3_key_prefix": "test/integration"}, "")
        print(f"test results: {json.dumps(results, indent=3, default=str)}")

        # Assert
        self.assertEqual(
            results[0]["reminder"]["name"], "integration lambda test - Take medicine"
        )

    def test_should_send_necessary_reminders_given_timezones(self):
        # Arrange
        bucket = "twilio-apps"
        os.environ["S3_BUCKET"] = bucket
        key_prefix = "test/integation-timezone-a"
        os.environ["S3_KEY_PREFIX"] = key_prefix
        s3 = S3()
        old_file_to_delete = f"{key_prefix}/reminders.json"
        print(f"Deleting {old_file_to_delete}")
        s3.delete_object(bucket, old_file_to_delete)

        repo = S3Repo(bucket, key_prefix, s3)
        few_mins_ago = datetime.now() - timedelta(minutes=3)
        alarm_time = few_mins_ago.strftime("%H:%M")
        print(f"Testing with alarm time {alarm_time}")
        repo.save_reminder(
            Reminder(
                "integration lambda test with timezone - Wash car 🚙",
                [alarm_time],
                ["+19193229617"],
            )
        )

        # Act
        # send several reminders to show the occurrences increase
        results = lambda_handler({"s3_key_prefix": key_prefix}, "")

        # Assert
        self.assertEqual(
            results[0]["reminder"]["name"],
            "integration lambda test with timezone - Wash car 🚙",
        )

    def test_should_send_not_necessary_reminders_given_timezones(self):
        # Arrange
        bucket = "twilio-apps"
        os.environ["S3_BUCKET"] = bucket
        key_prefix = "test/integation-timezone-b"
        os.environ["S3_KEY_PREFIX"] = key_prefix
        s3 = S3()
        old_file_to_delete = f"{key_prefix}/reminders.json"
        print(f"Deleting {old_file_to_delete}")
        s3.delete_object(bucket, old_file_to_delete)

        repo = S3Repo(bucket, key_prefix, s3)
        few_mins_ahead = datetime.now() + timedelta(minutes=3)
        alarm_time = few_mins_ahead.strftime("%H:%M")
        print(f"Testing with alarm time {alarm_time}")
        repo.save_reminder(
            Reminder(
                "integration lambda test with timezone - Wash car 🚙",
                [alarm_time],
                ["+19193229617"],
            )
        )

        # Act
        # send several reminders to show the occurrences increase
        results = lambda_handler({"s3_key_prefix": key_prefix}, "")

        # Assert
        self.assertEqual(
            len(results),
            0,
        )


if __name__ == "__main__":
    unittest.main()
