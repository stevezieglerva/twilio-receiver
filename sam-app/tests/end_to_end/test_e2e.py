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

        s3.delete_object(bucket, f"{key_prefix}/reminders.json")
        repo = S3Repo(bucket, key_prefix, s3)
        repo.save_reminder(Reminder("Take medicine", ["00:00"]))

        # Act
        l = boto3.client("lambda")
        results = l.invoke(FunctionName="twilio-send-reminders-test", Payload=b"{}")
        payload = results["Payload"].read()
        payload_json = json.loads(payload)
        print(f"test results: {json.dumps(payload_json, indent=3, default=str)}")

        # Assert
        self.assertEqual(payload_json[0]["name"], "Take medicine")


if __name__ == "__main__":
    unittest.main()
