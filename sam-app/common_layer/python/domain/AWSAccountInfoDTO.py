import dataclasses
import os
from dataclasses import dataclass

import boto3


@dataclass(frozen=True)
class AWSAccountInfoDTO:
    account_number: str
    proj_abbr: str

    @classmethod
    def create_from_dict(cls, object_json: dict):
        dataclass_fields = dataclasses.fields(cls)
        expected_fields = [field.name for field in dataclass_fields]
        constructor_arguments = []
        for field in expected_fields:
            try:
                field_value = object_json[field]
                constructor_arguments.append(field_value)
            except KeyError as e:
                # missing field might be optional so let it pass
                pass
        return cls(*constructor_arguments)

    @classmethod
    def create_from_env_info(cls):
        sts = boto3.client("sts")
        results = sts.get_caller_identity()
        return cls(results["Account"], os.environ["PROJ_ABBR"])
