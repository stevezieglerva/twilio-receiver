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
        reminders_db = self.get_all_data()
        current_reminders = reminders_db.reminders
        other_reminders = [r for r in current_reminders if r.name != reminder.name]
        new_reminders = other_reminders + [reminder]
        new_db = RemindersDB(reminders=new_reminders)
        data_json = json.dumps(asdict(new_db))
        self._s3.put_object(self._bucket_name, self._db_key, data_json)
        print(f"Update DB at self.db_key: {self._db_key}")

    def get_reminders(self) -> list:
        reminder_db = self.get_all_data()
        return reminder_db.reminders

    def get_reminder(self, name: str) -> RemindersDTO.Reminder:
        reminders = self.get_reminders()
        for reminder in reminders:
            if reminder.name == name:
                return reminder
        return None

    def get_all_data(self) -> RemindersDB:
        print(f"db_key: {self._db_key}")
        try:
            data = self._s3.get_object(self._bucket_name, self._db_key)
        except FileNotFoundError:
            return RemindersDB(reminders=[])
        data_json = json.loads(data)
        reminders_list = [RemindersDTO.Reminder(**r) for r in data_json["reminders"]]
        return RemindersDB(reminders=reminders_list)
