import json
import os

print(os.environ["PYTHONPATH"])

import Clock
import RemindersDTO
import ReminderSender
import StorageRepo

import SendAdapter


def lambda_handler(event, context):
    print(f"event: {event}")
    bucket = os.environ["S3_BUCKET"]
    print(f"bucket: {bucket}")
    key_prefix = os.environ["S3_KEY_PREFIX"]
    print(f"key_prefix: {key_prefix}")

    config = RemindersDTO.RemindersConfig()
    config.add_reminder(
        "Take medicine",
        ["09:00", "10:00"],
    )
    clock = Clock.RealClock()
    repo = StorageRepo.S3Repo(bucket, key_prefix)
    reminder_sender = ReminderSender.ReminderSender(config, clock, repo)

    subject = SendAdapter.SendAdapter(reminder_sender)
    results = subject.send_reminders()
    print(f"reminders sent: {json.dumps(results, indent=3, default=str)}")
    return results
