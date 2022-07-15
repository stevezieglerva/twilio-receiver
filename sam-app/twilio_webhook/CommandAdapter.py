import urllib.parse

from domain.SMSCommandDTO import *
from domain.SMSCommandProcessor import *


class CommandAdapter:
    def __init__(self, sms_command_processor: SMSCommandProcessor):
        self._sms_command_processor = sms_command_processor

    def process_command(self, event: dict) -> SMSCommandResult:
        twilio_text_body = event.get("body", "")
        body_fields = twilio_text_body.split("&")
        body_encoded = [f for f in body_fields if f.startswith("Body=")][0]
        body_encoded = body_encoded.replace("Body=", "")
        body = urllib.parse.unquote(body_encoded)
        print(f"body: {body}")

        from_phone_number_encoded = [f for f in body_fields if f.startswith("From=")][0]
        from_phone_number_encoded = from_phone_number_encoded.replace("From=", "")
        from_phone_number = urllib.parse.unquote(from_phone_number_encoded)
        print(f"from_phone_number: {from_phone_number}")

        sms_id_encoded = [f for f in body_fields if f.startswith("SmsMessageSid=")][0]
        sms_id_encoded = sms_id_encoded.replace("SmsMessageSid=", "")
        sms_id = urllib.parse.unquote(sms_id_encoded)
        print(f"sms_id: {sms_id}")

        results = self._sms_command_processor.process_command(
            SMSCommand(body, from_phone_number, sms_id)
        )
        print(results)
        return results
