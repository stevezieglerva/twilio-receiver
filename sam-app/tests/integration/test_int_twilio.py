import base64
import json
import os
import unittest
from datetime import datetime
from unittest.mock import MagicMock, Mock, PropertyMock, patch

import boto3
from botocore.exceptions import ClientError
from infrastructure.notifications.TwilioClient import *


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


class TwilioUnitTests(unittest.TestCase):
    def test_should_send_text(self):
        # Arrange
        keys = json.loads(get_secret("twilio"))
        print(keys)
        print(type(keys))
        account_sid = keys["TWILIO_ACCOUNT_SID"]
        auth_token = keys["TWILIO_AUTH_TOKEN"]
        subject = Twilio(account_sid, auth_token)

        # Act
        google_voice_number = "+19193229617"
        results = subject.send_text(
            google_voice_number, f"Here's a test message at {datetime.now()}"
        )
        print(f"test results: {results}")

        # Assert
        self.assertTrue(results.confirmation != "")


if __name__ == "__main__":
    unittest.main()
