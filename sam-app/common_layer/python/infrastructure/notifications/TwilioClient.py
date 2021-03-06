from abc import ABC, abstractclassmethod
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import List

from twilio.rest import Client


@dataclass(frozen=True)
class SMSText:
    phone_number: str
    text: str
    date: str
    confirmation: str = ""


class IProcessingTexts(ABC):
    @abstractclassmethod
    def send_text(self, phone_number: str, text: str) -> SMSText:
        raise NotImplementedError()

    @abstractclassmethod
    def receive_text(self, raw_webhook_body: str) -> str:
        raise NotImplementedError()


class FakeTwilio(IProcessingTexts):
    def __init__(self, twilio_acount_sid: str, twilio_auth_token: str):
        self._twilio_acount_sid = twilio_acount_sid
        self._twilio_auth_token = twilio_auth_token

    def send_text(self, phone_number: str, text: str) -> SMSText:
        filename = f"text_fake_{phone_number}_{datetime.now().isoformat()}.txt"
        with open(filename, "w") as file:
            file.write(text)

        return SMSText(
            phone_number, text, datetime.now().isoformat(), "fake-confirmation"
        )

    def receive_text(self, raw_webhook_body: str) -> str:
        return ""


class Twilio(IProcessingTexts):
    def __init__(self, twilio_acount_sid: str, twilio_auth_token: str):
        self._twilio_acount_sid = twilio_acount_sid
        self._twilio_auth_token = twilio_auth_token
        self._client = Client(twilio_acount_sid, twilio_auth_token)

    def send_text(self, phone_number: str, text: str) -> SMSText:
        print(f"About to text {phone_number} with {text}")
        message = self._client.messages.create(
            body=text,
            from_="+19894655460",
            to=phone_number,
        )
        print(message.sid)
        return SMSText(phone_number, text, datetime.now().isoformat(), message.sid)

    def receive_text(self, raw_webhook_body: str) -> str:
        return ""
