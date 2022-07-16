import unittest
from unittest.mock import MagicMock, Mock, PropertyMock, patch

from domain.SMSCommandDTO import *
from domain.SMSCommandProcessor import SMSCommandProcessor
from infrastructure.notifications.TwilioClient import *
from infrastructure.repository.S3 import *
from infrastructure.repository.StorageRepo import *
from infrastructure.system.Clock import *


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
            results.result_details, "✅ 'Take medicine' marked as done by +123456789."
        )

    def test_should_handle_mixed_case(self):
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
                body="DONE", from_phone_number="+123456789", sms_message_id="12345"
            )
        )
        print(f"test results: {results}")

        # Assert
        self.assertEqual(results.command.body, "DONE")
        self.assertEqual(results.result, "ok")
        self.assertEqual(
            results.result_details, "✅ 'Take medicine' marked as done by +123456789."
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

    def test_should_return_error_if_unknown_command(self):
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
                body="dkskdskd", from_phone_number="+123456789", sms_message_id="12345"
            )
        )
        print(f"test results: {results}")

        # Assert
        self.assertEqual(results.result, "error")
        self.assertEqual(
            results.result_details, "⁉️ 'dkskdskd' is an unknown commmand."
        )


if __name__ == "__main__":
    unittest.main()
