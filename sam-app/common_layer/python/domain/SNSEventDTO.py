from dataclasses import dataclass


EVENT_NAME_AWS_LOGIN_FAILURE = "aws_login_failure"
EVENT_NAME_SECURITY_CONCERN_ENDED = "security_concern_ended"


@dataclass(frozen=True)
class SNSEventDTO:
    source: str
    name: str
    message: str
    subject: str = ""

    def get_formatted_line(self):
        line = f"{self.source:<45}  {self.name:<40} "
        process_id = self.message.get("process_id", "")
        if process_id != "":
            line = line + f" {process_id:<40} "
        process_name = self.message.get("process_name", "")
        if process_name != "":
            line = line + f" {process_name:<40} "
        task_name = self.message.get("task_name", "")
        if task_name != "":
            line = line + f" {task_name:<40}"
        return line

    @classmethod
    def create_from_dict(cls, object_json: dict):
        dataclass_fields = dataclasses.fields(cls)
        print(json.dumps(dataclass_fields, indent=3, default=str))
        expected_fields = [field.name for field in dataclass_fields]
        constructor_arguments = []
        for field in expected_fields:
            try:
                field_value = object_json[field]
                constructor_arguments.append(field_value)
            except KeyError as e:
                # missing field might be optional so let it pass
                pass
        print(constructor_arguments)
        return cls(*constructor_arguments)
