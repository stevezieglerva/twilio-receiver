import unittest
from datetime import timedelta
from unittest.mock import MagicMock, Mock, PropertyMock, patch

import Clock
import RemindersDTO
import ReminderSender
import StorageRepo
from SMSCommandProcessor import *
from TwilioClient import *


class RemindersUnitTests(unittest.TestCase):
    # def test_should_send_text_if_time_right(self):
    #     # Arrange

    #     clock = Clock.FakeClock("2020-01-01 10:00:01")
    #     few_mins_ago = clock.get_time() - timedelta(minutes=3)
    #     repo = StorageRepo.FakeRepo()
    #     repo.save_reminder(RemindersDTO.Reminder("Take medicine", ["05:00"], ["444"]))
    #     twilio = FakeTwilio("abc", "123")
    #     subject = ReminderSender.ReminderSender(clock, repo, twilio)

    #     # Act
    #     results = subject.send_needed_reminder_texts()
    #     print(f"test results: {results}")

    #     # Assert
    #     self.assertEqual(results[0].reminder.name, "Take medicine")
    #     self.assertEqual(results[0].sms_texts[0].phone_number, "444")

    # def test_should_send_text_two_numbers_if_time_right(self):
    #     # Arrange

    #     clock = Clock.FakeClock("2020-01-01 10:00:01")
    #     few_mins_ago = clock.get_time() - timedelta(minutes=3)
    #     repo = StorageRepo.FakeRepo()
    #     repo.save_reminder(
    #         RemindersDTO.Reminder("Take medicine", ["05:00"], ["444", "555"])
    #     )
    #     twilio = FakeTwilio("abc", "123")
    #     subject = ReminderSender.ReminderSender(clock, repo, twilio)

    #     # Act
    #     results = subject.send_needed_reminder_texts()
    #     print(f"test results: {results}")

    #     # Assert
    #     self.assertEqual(results[0].sms_texts[1].phone_number, "555")

    # def test_should_send_not_text_if_time_wrong(self):
    #     # Arrange

    #     clock = Clock.FakeClock("2020-01-01 09:59:59")
    #     repo = StorageRepo.FakeRepo()
    #     repo.save_reminder(RemindersDTO.Reminder("Take medicine", ["05:00"], ["666"]))
    #     twilio = FakeTwilio("abc", "123")
    #     subject = ReminderSender.ReminderSender(clock, repo, twilio)

    #     # Act
    #     results = subject.send_needed_reminder_texts()
    #     print(f"test results: {results}")

    #     # Assert
    #     self.assertEqual(len(results), 0)

    # def test_should_activate_reminder_when_texted(self):
    #     # Arrange

    #     clock = Clock.FakeClock("2020-01-01 10:00:01")
    #     repo = StorageRepo.FakeRepo()
    #     repo.save_reminder(
    #         RemindersDTO.Reminder("Take medicine", ["05:00", "10:00"], ["777"])
    #     )
    #     twilio = FakeTwilio("abc", "123")
    #     subject = ReminderSender.ReminderSender(clock, repo, twilio)

    #     # Act
    #     results = subject.send_needed_reminder_texts()
    #     print(f"test results: {results}")

    #     # Assert
    #     self.assertEqual(
    #         results[0].reminder.status, RemindersDTO.ReminderStatuses.ACTIVE
    #     )
    #     self.assertTrue(results[0].reminder.last_sent is not None)
    #     self.assertEqual(results[0].reminder.occurences, 1)

    # def test_should_save_activated_reminder_in_repo(self):
    #     # Arrange

    #     clock = Clock.FakeClock("2020-01-01 10:00:01")
    #     repo = StorageRepo.FakeRepo()
    #     repo.save_reminder(
    #         RemindersDTO.Reminder("Take medicine", ["05:00", "10:00"], ["999"])
    #     )
    #     twilio = FakeTwilio("abc", "123")
    #     subject = ReminderSender.ReminderSender(clock, repo, twilio)

    #     # Act
    #     results = subject.send_needed_reminder_texts()
    #     print(f"test results: {results}")

    #     # Assert
    #     saved_reminder = repo.get_reminder("Take medicine")
    #     self.assertEqual(saved_reminder.status, RemindersDTO.ReminderStatuses.ACTIVE)

    # def test_should_not_send_if_reminder_is_done(self):
    #     # Arrange

    #     clock = Clock.FakeClock("2020-01-01 10:00:01")
    #     repo = StorageRepo.FakeRepo()
    #     repo.save_reminder(
    #         RemindersDTO.Reminder(
    #             "Pick up kids",
    #             ["05:00", "10:00"],
    #             ["000"],
    #             status=RemindersDTO.ReminderStatuses.DONE,
    #         )
    #     )
    #     twilio = FakeTwilio("abc", "123")
    #     subject = ReminderSender.ReminderSender(clock, repo, twilio)

    #     # Act
    #     results = subject.send_needed_reminder_texts()
    #     print(f"test results: {results}")

    #     # Assert
    #     self.assertEqual(results, [])

    def test_should_stop_sending_when_marked_done(self):
        # Arrange

        clock_10AM = Clock.FakeClock("2020-01-01 15:00:01")
        s3 = S3FakeLocal()
        repo = StorageRepo.S3Repo("fake-bucket", "test/unit-test/second_time", s3)
        repo.save_reminder(
            RemindersDTO.Reminder("Take medicine", ["10:00", "13:00"], ["444"])
        )
        twilio = FakeTwilio("abc", "123")
        initial_sender = ReminderSender.ReminderSender(clock_10AM, repo, twilio)

        # Send first 10AM reminder and mark done
        results = initial_sender.send_needed_reminder_texts()
        command_proc = SMSCommandProcessor(repo, clock_10AM, twilio)
        results = command_proc.process_command(SMSCommand("done", "444", "789"))

        # Act
        results = initial_sender.send_needed_reminder_texts()

        print(f"test results: {results}")

        # Assert
        self.assertEqual(len(results), 0)

    # def test_should_send_second_reminder_if_first_marked_done(self):
    #     # Arrange

    #     clock_10AM = Clock.FakeClock("2020-01-01 15:00:01")
    #     s3 = S3FakeLocal()
    #     repo = StorageRepo.S3Repo("fake-bucket", "test/unit-test/second_time", s3)
    #     repo.save_reminder(
    #         RemindersDTO.Reminder("Take medicine", ["10:00", "13:00"], ["444"])
    #     )
    #     twilio = FakeTwilio("abc", "123")
    #     initial_sender = ReminderSender.ReminderSender(clock_10AM, repo, twilio)

    #     # Send first 10AM reminder and mark done
    #     results = initial_sender.send_needed_reminder_texts()
    #     command_proc = SMSCommandProcessor(repo, clock_10AM, twilio)
    #     results = command_proc.process_command(SMSCommand("done", "444", "789"))

    #     # Act
    #     clock_1PM = Clock.FakeClock("2020-01-01 17:00:01")
    #     subject = ReminderSender.ReminderSender(clock_1PM, repo, twilio)
    #     results = subject.send_needed_reminder_texts()

    #     print(f"test results: {results}")

    #     # Assert
    #     self.assertEqual(results[0].reminder.name, "Take medicine")
    #     self.assertEqual(results[0].sms_texts[0].phone_number, "444")


if __name__ == "__main__":
    unittest.main()
