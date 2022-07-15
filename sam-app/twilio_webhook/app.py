import base64
import json
from dataclasses import asdict, dataclass
from email.mime import base

from domain.SMSCommandDTO import *
from domain.SMSCommandProcessor import SMSCommandProcessor
from infrastructure.notifications.TwilioClient import *
from infrastructure.repository.S3 import *
from infrastructure.repository.StorageRepo import *
from infrastructure.system.Clock import *

from CommandAdapter import CommandAdapter


def lambda_handler(event, context):
    print("Starting ...")
    clock = RealClock()
    log_starting_info(event, clock)

    print(f"event: {event}")
    bucket = os.environ["S3_BUCKET"]
    print(f"bucket: {bucket}")

    key_prefix = get_correct_key_prefix(event)

    s3 = S3()
    repo = S3Repo(bucket, key_prefix, s3)

    twilio = configure_twilio()

    command_processor = SMSCommandProcessor(repo, clock, twilio)
    adapter = CommandAdapter(command_processor)
    results = adapter.process_command(event)

    return {
        "statusCode": 200,
    }


def log_starting_info(event, clock):
    now_gmt = clock.get_time()
    print(f"now_gmt:  {now_gmt}")
    now_est = clock.get_time("America/New_York")
    print(f"now_est:  {now_est}")
    print(json.dumps(event, indent=3, default=str))


def configure_twilio():
    keys = json.loads(get_secret("twilio"))
    account_sid = keys["TWILIO_ACCOUNT_SID"]
    auth_token = keys["TWILIO_AUTH_TOKEN"]
    twilio = Twilio(account_sid, auth_token)
    return twilio


def get_correct_key_prefix(event):
    key_prefix = os.environ["S3_KEY_PREFIX"]
    print(f"key_prefix: {key_prefix}")
    key_prefix_from_event = event.get("s3_key_prefix", "")
    if key_prefix_from_event != "":
        print(f"key_prefix_from_event pased in: {key_prefix_from_event}")
        key_prefix = key_prefix_from_event
    return key_prefix


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
