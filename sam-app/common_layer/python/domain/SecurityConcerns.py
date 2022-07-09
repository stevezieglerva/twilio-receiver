import json
import os
from dataclasses import dataclass
from datetime import datetime
from typing import List
from botocore import discovery
from botocore.retryhandler import delay_exponential

from ulid import ULID

from domain.IManageSecurityConcerns import *
from domain.SecurityConcernDTO import *
from infrastructure.repository.IRepository import IRepository
from infrastructure.notifications.INotifier import INotifier
from infrastructure.aws.IAWSApis import *
from domain.SNSEventDTO import *
from domain.AWSAccountInfoDTO import *


class SecurityConcerns(IManageSecurityConcerns):
    def __init__(
        self,
        repository: IRepository,
        notifier: INotifier,
        aws_info: AWSAccountInfoDTO,
        aws_apis: IAWSApis,
    ):
        self.repository = repository
        self.notifier = notifier
        self.aws_info = aws_info
        self.aws_apis = aws_apis

    def create_security_concern(
        self,
        name,
    ) -> SecurityConcernDTO:

        print("Creating new concern")
        notification_count = 1
        new_concern = create_security_concern_dto(
            self.aws_apis,
            name,
            str(ULID()),
            datetime.now().isoformat(),
            "",
            "",
            notification_count,
        )
        print(f"type: {type(new_concern)}")
        self.repository.save_security_concern(new_concern)

        event = new_concern.create_notification(
            "SecurityConcerns",
            self.aws_info,
        )
        self.notifier.send_message(event)
        return SecurityConcernNotificationResponse(new_concern, event)

    def end_security_concern(self, id: str, ended_by: str) -> SecurityConcernDTO:
        original_security_concern = self.repository.get_security_concern(id)
        updated_concern = SecurityConcernDTO(
            original_security_concern.name,
            original_security_concern.id,
            original_security_concern.started,
            datetime.now().isoformat(),
            ended_by,
            original_security_concern.number_of_alerts_sent,
            original_security_concern.context_of_issue,
            original_security_concern.log_group,
        )

        self.repository.save_security_concern(updated_concern)
        self.repository.delete_security_concern(original_security_concern)

        subject = f"✅🔐 Security concern ended for {updated_concern.name}"
        message = f"""The security concern has ended. 
        
Details:
   Alarm Name:  {updated_concern.name}
   ID:          {updated_concern.id}
   Started:     {updated_concern.started}
   Ended:       {updated_concern.ended}

   AWS Account: {self.aws_info.account_number}
   Project:     {self.aws_info.proj_abbr}
"""
        event = SNSEventDTO(
            "SecurityConcern",
            EVENT_NAME_SECURITY_CONCERN_ENDED,
            message,
            subject,
        )
        self.notifier.send_message(event)
        return SecurityConcernNotificationResponse(updated_concern, event)

    def send_alerts_for_open_concerns(self) -> list:
        results = []
        open_security_concerns = self.repository.get_open_security_concerns()

        for open_security_concern in open_security_concerns:
            new_notification_count = open_security_concern.number_of_alerts_sent + 1
            increased_notification_count_concern = get_security_concern_dto(
                open_security_concern.name,
                open_security_concern.id,
                open_security_concern.started,
                open_security_concern.ended,
                open_security_concern.ended_by,
                new_notification_count,
                open_security_concern.context_of_issue,
                open_security_concern.log_group,
            )
            self.repository.save_security_concern(increased_notification_count_concern)
            event = open_security_concern.create_notification(
                "SecurityConcerns",
                self.aws_info,
            )
            self.notifier.send_message(event)
            concern_result = SecurityConcernNotificationResponse(
                increased_notification_count_concern, event
            )
            results.append(concern_result)
        return results
