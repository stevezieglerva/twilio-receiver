import unittest
from unittest.mock import MagicMock, Mock, PropertyMock, patch

from domain.SMSCommandDTO import *
from domain.SMSCommandProcessor import SMSCommandProcessor
from infrastructure.notifications.TwilioClient import *
from infrastructure.repository.S3 import *
from infrastructure.repository.StorageRepo import *
from infrastructure.system.Clock import *
from twilio_webhook.app import *
from twilio_webhook.CommandAdapter import *


class CommandAdapterUnitTests(unittest.TestCase):
    def test_should_process_done(self):
        # Arrange
        clock = FakeClock("2020-01-01 10:00:01")
        s3 = S3FakeLocal()
        repo = S3Repo("fake-bucket", "unit-test", s3)
        repo.save_reminder(
            Reminder(
                "Take medicine", ["05:00"], ["444"], status=ReminderStatuses.ACTIVE
            )
        )
        twilio = FakeTwilio("abc", "123")
        sms_command_processor = SMSCommandProcessor(repo, clock, twilio)

        subject = CommandAdapter(sms_command_processor)

        # Act
        # Act
        results = subject.process_command(
            {
                "body": "ToCountry=US&ToState=MI&SmsMessageSid=SM99649d01253fc588396cd1eec8377273&NumMedia=0&ToCity=COLEMAN&FromZip=22036&SmsSid=SM99649d01253fc588396cd1eec8377273&FromState=VA&SmsStatus=received&FromCity=CENTREVILLE&Body=done&FromCountry=US&To=%2B19894655460&ToZip=48612&NumSegments=1&ReferralNumMedia=0&MessageSid=SM99649d01253fc588396cd1eec8377273&AccountSid=ACec8e197bef5e214e76eecfabee4107cc&From=%2B17039750614&ApiVersion=2010-04-01"
            }
        )
        print(f"test results: {results}")

        # Assert
        self.assertEqual(results.command.body, "done")
        self.assertEqual(results.result, "ok")
        self.assertEqual(
            results.result_details, "✅ 'Take medicine' marked as done by +17039750614."
        )


if __name__ == "__main__":
    unittest.main()
