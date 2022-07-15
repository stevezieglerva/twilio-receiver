import unittest
from unittest.mock import MagicMock, Mock, PropertyMock, patch

from domain.SMSCommandDTO import *
from domain.SMSCommandProcessor import SMSCommandProcessor
from infrastructure.notifications.TwilioClient import *
from infrastructure.repository.S3 import *
from infrastructure.repository.StorageRepo import *
from infrastructure.system.Clock import *


def get_secret(secret_name: str):
    secret_name = secret_name
    region_name = "us-east-1"
    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region_name)

    get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    if "SecretString" in get_secret_value_response:
        secret = get_secret_value_response["SecretString"]
        return secret
    else:
        decoded_binary_secret = base64.b64decode(
            get_secret_value_response["SecretBinary"]
        )
        return decoded_binary_secret


class SMSCommandProcessorUnitTests(unittest.TestCase):
    def test_should_return_inactive_info_when_done_sent(self):
        # Arrange
        clock = RealClock()

        s3 = S3()
        repo = S3Repo("twilio-apps", "integration_testing_commands_a", s3)
        repo.save_reminder(
            Reminder(
                "Take medicine",
                ["05:00"],
                ["+19193229617"],
                status=ReminderStatuses.ACTIVE,
            )
        )

        keys = json.loads(get_secret("twilio"))
        account_sid = keys["TWILIO_ACCOUNT_SID"]
        auth_token = keys["TWILIO_AUTH_TOKEN"]
        twilio = Twilio(account_sid, auth_token)

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
        self.assertEqual(results.result_details, "'dkskdskd' is an unknown commmand.")


if __name__ == "__main__":
    unittest.main()
