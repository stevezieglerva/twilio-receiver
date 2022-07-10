import json
from abc import ABC, abstractclassmethod
from dataclasses import asdict, dataclass
from typing import List

import RemindersDTO

import S3


@dataclass(frozen=True)
class RemindersDB:
    reminders: List[RemindersDTO.Reminder]


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

    @abstractclassmethod
    def get_all_data(self) -> RemindersDB:
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

    def get_all_data(self) -> RemindersDB:
        return RemindersDB(field="fake", reminders=self._reminders)


class S3Repo(IStoringReminders):
    def __init__(self, bucket_name: str, key_prefix: str, s3: S3):
        self._reminders = []
        self._bucket_name = bucket_name
        self._key_prefix = key_prefix
        self._s3 = s3
        self._db_key = f"{self._key_prefix}/reminders_db.json"

    def save_reminder(self, reminder: RemindersDTO.Reminder) -> None:
        raise NotImplementedError

    def get_reminders(self) -> list:
        raise NotImplementedError

    def get_reminder(self, name: str) -> RemindersDTO.Reminder:
        raise NotImplementedError

    def get_all_data(self) -> RemindersDB:
        print(f"db_key: {self._db_key}")
        data = self._s3.get_object(self._bucket_name, self._db_key)
        data_json = json.loads(data)
        reminders_list = [RemindersDTO.Reminder(**r) for r in data_json["reminders"]]
        return RemindersDB(reminders=reminders_list)
