import unittest
from unittest.mock import MagicMock, Mock, PropertyMock, patch

from domain.SMSCommandDTO import *
from domain.SMSCommandProcessor import SMSCommandProcessor
from infrastructure.notifications.TwilioClient import *
from infrastructure.repository.S3 import *
from infrastructure.repository.StorageRepo import *
from infrastructure.system.Clock import *

# "ToCountry=US&
# ToState=MI&
# SmsMessageSid=SM99649d01253fc588396cd1eec8377273&NumMedia=0&
# ToCity=COLEMAN&
# FromZip=22036&
# SmsSid=SM99649d01253fc588396cd1eec8377273&
# FromState=VA&
# SmsStatus=received&
# FromCity=CENTREVILLE&
# Body=It%27s+working%21%21%21&
# FromCountry=US&
# To=%2B19894655460&
# ToZip=48612&
# NumSegments=1&
# ReferralNumMedia=0&
# MessageSid=SM99649d01253fc588396cd1eec8377273&
# AccountSid=ACec8e197bef5e214e76eecfabee4107cc&
# From=%2B17038250630&
# ApiVersion=2010-04-01",


class SMSCommandProcessorUnitTests(unittest.TestCase):
    def test_should_return_inactive_info_when_done_sent(self):
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
        subject = SMSCommandProcessor(repo, clock, twilio)

        # Act
        results = subject.process_command(
            SMSCommand(
                body="done", from_phone_number="+123456789", sms_message_id="12345"
            )
        )
        print(f"test results: {results}")

        # Assert
        self.assertEqual(results.command.body, "done")
        self.assertEqual(results.result, "ok")
        self.assertEqual(
            results.result_details, "'Take medicine' marked as done by +123456789."
        )

    def test_should_inactive_reminder_record_when_done_sent(self):
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
        subject = SMSCommandProcessor(repo, clock, twilio)

        # Act
        results = subject.process_command(
            SMSCommand(
                body="done", from_phone_number="+123456789", sms_message_id="12345"
            )
        )
        print(f"test results: {results}")

        # Assert
        updated_reminder = repo.get_reminder("Take medicine")
        self.assertEqual(updated_reminder.status, ReminderStatuses.INACTIVE)


if __name__ == "__main__":
    unittest.main()
