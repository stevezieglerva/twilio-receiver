import dataclasses
import json
from abc import abstractmethod
from dataclasses import dataclass

from infrastructure.aws.IAWSApis import IAWSApis

from domain.AWSAccountInfoDTO import *
from domain.SNSEventDTO import SNSEventDTO

ALARM_NAME_SSH_FAILED_LOGINS = "ops-aws-sec-conc-ssh-failed-login"
ALARM_NAME_AWS_FAILED_LOGINS = "ops-aws-sec-conc-aws-failed-login"


@dataclass(frozen=True)
class SecurityConcernDTO:
    name: str
    id: str
    started: str
    ended: str
    ended_by: str
    number_of_alerts_sent: int
    context_of_issue: str
    log_group: str

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

    @abstractmethod
    def create_notification(
        self,
        source: str,
        aws_info: AWSAccountInfoDTO,
    ) -> SNSEventDTO:
        raise NotImplemented


class SecConAWSLoginFailureDTO(SecurityConcernDTO):
    def create_notification(
        self,
        source: str,
        aws_info: AWSAccountInfoDTO,
    ) -> SNSEventDTO:
        subject = f"❌🔐 AWS Login Failures Alert in {aws_info.proj_abbr}"
        message = f"""Numerous failed logins occured in your AWS account. Please log in and review the user and delete the IAM account if necessary. To end the concern's regular emails, run the ops-aws-end-security-concern Lambda in the AWS Console passing in the list of IDs to end as the Lambda event (Ex: {{"id_list" : ["{self.id}"]}} ).

Details:
   Alarm Name:  {self.name}
   ID:          {self.id}
   Started:     {self.started}
   Alert Count: {self.number_of_alerts_sent}

   AWS Account: {aws_info.account_number}
   Project:     {aws_info.proj_abbr}

   Context:
{self.context_of_issue}
"""
        return SNSEventDTO(source, ALARM_NAME_AWS_FAILED_LOGINS, message, subject)


class SecConSSHLoginFailureDTO(SecurityConcernDTO):
    def create_notification(
        self, source: str, aws_info: AWSAccountInfoDTO
    ) -> SNSEventDTO:

        subject = f"❌🔐 SSH Login Failures Alert in {aws_info.proj_abbr}"
        message = f"""Numerous failed logins occured for an EC2 via SSH. Please log in and review the CloudWatch sys logs. To end the concern's regular emails, run the ops-aws-end-security-concern Lambda in the AWS Console passing in the list of IDs to end as the Lambda event (Ex: {{"id_list" : ["{self.id}"]}} ).

Details:
   Alarm Name:  {self.name}
   ID:          {self.id}
   Started:     {self.started}
   Alert Count: {self.number_of_alerts_sent}
   Log:         {self.log_group}

   AWS Account: {aws_info.account_number}
   Project:     {aws_info.proj_abbr}

   Context:
{self.context_of_issue}
"""

        return SNSEventDTO(source, ALARM_NAME_SSH_FAILED_LOGINS, message, subject)


def create_security_concern_dto(
    aws_apis: IAWSApis,
    name: str,
    id: str,
    started: str,
    ended: str,
    ended_by: str,
    number_of_alerts_sent: int,
) -> SecurityConcernDTO:
    if name.startswith(ALARM_NAME_AWS_FAILED_LOGINS):
        return SecConAWSLoginFailureDTO(
            name,
            id,
            started,
            ended,
            ended_by,
            number_of_alerts_sent,
            "Not coded yet",
            "NA",
        )
    if name.startswith(ALARM_NAME_SSH_FAILED_LOGINS):
        alarm_name = name.split("/")[0]
        alarm = aws_apis.get_alarm(alarm_name)
        print(f"alarm: {alarm}")
        recent_log_lines = aws_apis.filter_log_events(
            alarm.log_filter.log_group_name, "Invalid"
        )
        first_few_lines = recent_log_lines[0:3]
        print(f"recent_log_lines: {first_few_lines}")
        recent_log_lines_text = "\n".join(first_few_lines)

        return SecConSSHLoginFailureDTO(
            name,
            id,
            started,
            ended,
            ended_by,
            number_of_alerts_sent,
            recent_log_lines_text,
            alarm.log_filter.log_group_name,
        )
    raise ValueError(f"Unknown alarm type: {name}")


def get_security_concern_dto(
    name: str,
    id: str,
    started: str,
    ended: str,
    ended_by: str,
    number_of_alerts_sent: int,
    context_of_issue: str,
    log_group: str,
) -> SecurityConcernDTO:
    if name.startswith(ALARM_NAME_AWS_FAILED_LOGINS):
        return SecConAWSLoginFailureDTO(
            name,
            id,
            started,
            ended,
            ended_by,
            number_of_alerts_sent,
            context_of_issue,
            log_group,
        )
    if name.startswith(ALARM_NAME_SSH_FAILED_LOGINS):
        return SecConSSHLoginFailureDTO(
            name,
            id,
            started,
            ended,
            ended_by,
            number_of_alerts_sent,
            context_of_issue,
            log_group,
        )
    raise ValueError(f"Unknown alarm type: {name}")
