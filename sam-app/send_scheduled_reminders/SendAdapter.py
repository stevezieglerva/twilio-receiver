from argparse import RawDescriptionHelpFormatter

from domain.ReminderSender import *


class SendAdapter:
    def __init__(self, reminder_sender: ReminderSender) -> None:
        self._reminder_sender = reminder_sender

    def send_reminders(self) -> None:
        return self._reminder_sender.send_needed_reminder_texts()
