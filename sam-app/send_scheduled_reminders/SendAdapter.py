from argparse import RawDescriptionHelpFormatter

import ReminderSender


class SendAdapter:
    def __init__(self, reminder_sender: ReminderSender.ReminderSender) -> None:
        pass

    def send_reminders(self) -> None:
        return []
