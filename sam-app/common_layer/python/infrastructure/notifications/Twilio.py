from abc import ABC, abstractclassmethod
from dataclasses import asdict, dataclass
from typing import List


@dataclass(frozen=True)
class Text:
    phone_numbers: List[str]
    text: str
    date: str


class IProcessingTexts(ABC):
    @abstractclassmethod
    def send_text(self, phone_number: str, text: str) -> str:
        raise NotImplementedError()

    @abstractclassmethod
    def receive_text(self, raw_webhook_body: str) -> str:
        raise NotImplementedError()


class FakeTwilio(IProcessingTexts):
    def __init__(self, twilio_acount_sid: str, twilio_auth_token: str):
        self._twilio_acount_sid = twilio_acount_sid
        self._twilio_auth_token = twilio_auth_token

    def send_text(self, phone_number: str, text: str) -> str:
        return ""

    def receive_text(self, raw_webhook_body: str) -> str:
        return ""
