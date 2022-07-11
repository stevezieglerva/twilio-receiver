import json

import Clock
import RemindersDTO
import ReminderSender
import StorageRepo

import SendAdapter


def lambda_handler(event, context):
    print(f"event: {event}")

    clock = Clock.RealClock()
    repo = StorageRepo.S3Repo("x", "ci_test")
    repo.save_reminder(RemindersDTO.Reminder("Take medicine", ["09:00", "10:00"]))
    reminder_sender = ReminderSender.ReminderSender(config, clock, repo)

    subject = SendAdapter.SendAdapter(reminder_sender)
    results = subject.send_reminders()
    print(f"reminders sent: {json.dumps(results, indent=3, default=str)}")
    return results
