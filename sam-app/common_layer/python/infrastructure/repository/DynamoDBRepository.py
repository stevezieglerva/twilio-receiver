import json

import boto3
from domain.SecurityConcernDTO import *
from infrastructure.repository.DynamoDB import DynamoDB, RecordNotFound
from infrastructure.repository.IRepository import IRepository

PK_OPEN = "SECURITY_CONCERN_STATUS#OPEN"
PK_CLOSED = "SECURITY_CONCERN_STATUS#CLOSED"


class DynamoDBRepository(IRepository):
    def __init__(self, source):
        self.db = DynamoDB(source)
        seconds_in_24_hours = 60 * 60 * 24

    def get_security_concern(self, id: str) -> SecurityConcernDTO:
        try:
            json_data = self.db.get_item(
                {"pk": PK_OPEN, "sk": f"SECURITY_CONCERN#{id}"}
            )
        except RecordNotFound:
            json_data = self.db.get_item(
                {"pk": PK_CLOSED, "sk": f"SECURITY_CONCERN#{id}"}
            )
        except Exception as e:
            raise e

        return SecurityConcernDTO.create_from_dict(json_data)

    def save_security_concern(self, security_concern: SecurityConcernDTO) -> dict:
        db_record = security_concern.__dict__.copy()
        db_record["pk"] = self._get_pk(security_concern.ended)
        db_record["sk"] = f"SECURITY_CONCERN#{security_concern.id}"
        print(f"Saving: {db_record}")
        self.db.put_item(db_record)
        return db_record

    def get_open_security_concerns(self) -> list:
        open_concerns_json = self.db.query_table_begins(
            {"pk": PK_OPEN, "sk": "SECURITY_CONCERN"}
        )
        print(json.dumps(open_concerns_json, indent=3, default=str))
        open_concerns = []
        for open_concern in open_concerns_json:
            concern = get_security_concern_dto(
                open_concern["name"],
                open_concern["id"],
                open_concern["started"],
                open_concern["ended"],
                open_concern["ended_by"],
                open_concern["number_of_alerts_sent"],
                open_concern["context_of_issue"],
                open_concern["log_group"],
            )
            open_concerns.append(concern)
        return open_concerns

    def delete_security_concern(self, security_concern: SecurityConcernDTO):
        item_key = {}
        item_key["pk"] = self._get_pk(security_concern.ended)
        item_key["sk"] = f"SECURITY_CONCERN#{security_concern.id}"
        self.db.delete_item(item_key)

    def _get_pk(self, ended):
        if ended == "":
            return PK_OPEN
        return PK_CLOSED
