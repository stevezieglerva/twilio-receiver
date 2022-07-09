from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

from infrastructure.notifications.INotifier import INotifier
from infrastructure.repository.IRepository import IRepository
from infrastructure.aws.IAWSApis import IAWSApis

from domain.AWSAccountInfoDTO import *
from domain.SecurityConcernDTO import SecurityConcernDTO
from domain.SNSEventDTO import *


@dataclass(frozen=True)
class SecurityConcernNotificationResponse:
    security_concern: SecurityConcernDTO
    event: SNSEventDTO


class IManageSecurityConcerns(ABC):
    def __init__(
        self,
        repository: IRepository,
        notifier: INotifier,
        aws_info: AWSAccountInfoDTO,
        aws_apis: IAWSApis,
    ):
        raise NotImplemented

    @abstractmethod
    def create_security_concern(
        self,
        name: str,
    ) -> SecurityConcernNotificationResponse:
        raise NotImplemented

    @abstractmethod
    def end_security_concern(
        self,
        security_concern: SecurityConcernDTO,
    ) -> SecurityConcernNotificationResponse:
        raise NotImplemented

    def send_alerts_for_open_concerns(self) -> list:
        raise NotImplemented
