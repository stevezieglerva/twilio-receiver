import json
import os

python_path = os.environ.get("PYTHONPATH", "")
print(f"python_path: {python_path}")


from domain.RemindersDTO import *

print("import 1")
from domain.ReminderSender import *

print("import 2")
from infrastructure.repository.StorageRepo import *

print("import 3")
from infrastructure.system.Clock import *

print("import 4")


import SendAdapter


def lambda_handler(event, context):
    print(f"event: {event}")
    bucket = os.environ["S3_BUCKET"]
    print(f"bucket: {bucket}")
    key_prefix = os.environ["S3_KEY_PREFIX"]
    print(f"key_prefix: {key_prefix}")

    config = RemindersConfig()
    config.add_reminder(
        "Take medicine",
        ["09:00", "10:00"],
    )
    clock = RealClock()
    repo = S3Repo(bucket, key_prefix)
    reminder_sender = ReminderSender.ReminderSender(config, clock, repo)

    subject = SendAdapter.SendAdapter(reminder_sender)
    results = subject.send_reminders()
    print(f"reminders sent: {json.dumps(results, indent=3, default=str)}")
    return results
