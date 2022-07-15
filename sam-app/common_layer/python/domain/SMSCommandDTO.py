from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class SMSCommand:
    body: str
    from_phone_number: str
    sms_message_id: str
