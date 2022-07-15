from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class SMSCommand:
    body: str
    from_phone_number: str
    sms_message_id: str


class SMSCommands:
    DONE: str = "done"

    # "ToCountry=US&


# ToState=MI&
# SmsMessageSid=SM99649d01253fc588396cd1eec8377273&NumMedia=0&
# ToCity=COLEMAN&
# FromZip=22036&
# SmsSid=SM99649d01253fc588396cd1eec8377273&
# FromState=VA&
# SmsStatus=received&
# FromCity=CENTREVILLE&
# Body=It%27s+working%21%21%21&
# FromCountry=US&
# To=%2B19894655460&
# ToZip=48612&
# NumSegments=1&
# ReferralNumMedia=0&
# MessageSid=SM99649d01253fc588396cd1eec8377273&
# AccountSid=ACec8e197bef5e214e76eecfabee4107cc&
# From=%2B17038250630&
# ApiVersion=2010-04-01",
