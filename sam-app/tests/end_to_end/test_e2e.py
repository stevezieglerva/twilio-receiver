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
        key_prefix = "test/end_to_end"
        s3 = S3()

        s3.delete_object(bucket, f"{key_prefix}/reminders.json")
        repo = S3Repo(bucket, key_prefix, s3)
        repo.save_reminder(
            Reminder("e2e test - Take medicine", ["00:00"], ["19193229617"])
        )

        # Act
        l = boto3.client("lambda")
        results = l.invoke(
            FunctionName="twilio-send-reminders-test",
            Payload=b'{"s3_key_prefix" : "test/end_to_end"}',
        )
        payload = results["Payload"].read()
        payload_json = json.loads(payload)
        print(f"test results: {json.dumps(payload_json, indent=3, default=str)}")

        # Assert
        reminders_sent = [r["reminder"]["name"] for r in payload_json]
        self.assertTrue("e2e test - Take medicine" in reminders_sent)


if __name__ == "__main__":
    unittest.main()
