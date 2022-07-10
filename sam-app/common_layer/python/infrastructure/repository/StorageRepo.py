from abc import ABC, abstractclassmethod

import RemindersDTO

import S3


class IStoringReminders(ABC):
    @abstractclassmethod
    def save_reminder(self, reminder: RemindersDTO.Reminder) -> None:
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

    def save_reminder(self, reminder: str) -> None:
        other_reminders = [r for r in self._reminders if r.name != reminder.name]
        self._reminders = other_reminders + [reminder]

    def get_reminders(self) -> list:
        return self._reminders

    def get_reminder(self, name: str) -> RemindersDTO.Reminder:
        for reminder in self._reminders:
            if reminder.name == name:
                return reminder
        return None


class S3Repo(IStoringReminders):
    def __init__(self, bucket_name: str, key_prefix: str):
        self._reminders = []
        self._bucket_name = bucket_name
        self._key_prefix = key_prefix

    def save_reminder(self, reminder: RemindersDTO.Reminder) -> None:
        raise NotImplementedError

    def get_reminders(self) -> list:
        raise NotImplementedError

    def get_reminder(self, name: str) -> RemindersDTO.Reminder:
        raise NotImplementedError
