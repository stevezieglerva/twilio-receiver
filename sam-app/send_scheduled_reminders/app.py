import json
import os

python_path = os.environ.get("PYTHONPATH", "")
print(f"python_path: {python_path}")


from domain.RemindersDTO import *
from domain.ReminderSender import *
from infrastructure.repository.S3 import *
from infrastructure.repository.StorageRepo import *
from infrastructure.system.Clock import *

from SendAdapter import *


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
    s3 = S3()
    repo = S3Repo(bucket, key_prefix, s3)
    reminder_sender = ReminderSender(config, clock, repo)

    subject = SendAdapter(reminder_sender)
    results = subject.send_reminders()
    print(f"reminders sent: {json.dumps(results, indent=3, default=str)}")
    return results
