from abc import ABC, abstractclassmethod

import RemindersDTO


class IStoringReminders(ABC):
    @abstractclassmethod
    def store_reminder(self, reminder: RemindersDTO.Reminder) -> None:
        raise NotImplementedError()

    @abstractclassmethod
    def get_reminders(self) -> list:
        raise NotImplementedError()

    @abstractclassmethod
    def get_reminder(self, name: str) -> RemindersDTO.Reminder:
        raise NotImplementedError()


class FakeRepo(IStoringReminders):
    def __init__(self):
        self._reminders = []

    def store_reminder(self, reminder: RemindersDTO.Reminder) -> None:
        other_reminders = [r for r in self._reminders if r.name != reminder.name]
        self._reminders = other_reminders + [reminder]

    def get_reminders(self) -> list:
        return self._reminders

    def get_reminder(self, name: str) -> RemindersDTO.Reminder:
        for reminder in self._reminders:
            if reminder.name == name:
                return reminder
        return None
