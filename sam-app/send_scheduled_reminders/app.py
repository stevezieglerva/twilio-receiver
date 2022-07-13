import json
import os

python_path = os.environ.get("PYTHONPATH", "")
print(f"python_path: {python_path}")

import base64
from dataclasses import asdict

import boto3
from domain.RemindersDTO import *
from domain.ReminderSender import *
from infrastructure.notifications.TwilioClient import *
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

    clock = RealClock()
    s3 = S3()
    repo = S3Repo(bucket, key_prefix, s3)
    twilio_keys = get_secret("twilio")
    account_sid = twilio_keys["TWILIO_ACCOUNT_SID"]
    auth_token = twilio_keys["TWILIO_AUTH_TOKEN"]
    twilio = Twilio(account_sid, auth_token)
    reminder_sender = ReminderSender(clock, repo, twilio)

    subject = SendAdapter(reminder_sender)
    results = subject.send_reminders()
    print(f"reminders sent: {json.dumps(results, indent=3, default=str)}")
    return [asdict(r) for r in results]


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
