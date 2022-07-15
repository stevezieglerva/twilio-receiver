import unittest
from unittest.mock import MagicMock, Mock, PropertyMock, patch

from infrastructure.repository.S3 import *
from infrastructure.repository.StorageRepo import *
from twilio_webhook.app import *


class TwilioWebhookIntTests(unittest.TestCase):
    def test_should_process_done(self):
        # Arrange
        bucket = "twilio-apps"
        os.environ["S3_BUCKET"] = bucket
        key_prefix = "test/integration_lambda_webhood-a"
        os.environ["S3_KEY_PREFIX"] = key_prefix

        s3 = S3()
        repo = S3Repo("twilio-apps", key_prefix, s3)
        repo.save_reminder(
            Reminder(
                "Take medicine",
                ["05:00"],
                ["+19193229617"],
                status=ReminderStatuses.ACTIVE,
            )
        )

        # Act
        results = lambda_handler(
            {
                "body": "ToCountry=US&ToState=MI&SmsMessageSid=SM99649d01253fc588396cd1eec8377273&NumMedia=0&ToCity=COLEMAN&FromZip=22036&SmsSid=SM99649d01253fc588396cd1eec8377273&FromState=VA&SmsStatus=received&FromCity=CENTREVILLE&Body=done&FromCountry=US&To=%2B19894655460&ToZip=48612&NumSegments=1&ReferralNumMedia=0&MessageSid=SM99649d01253fc588396cd1eec8377273&AccountSid=ACec8e197bef5e214e76eecfabee4107cc&From=%2B17039750614&ApiVersion=2010-04-01"
            },
            "",
        )
        print(f"test results: {results}")

        # Assert
        self.assertEqual(results["statusCode"], 200)


if __name__ == "__main__":
    unittest.main()
