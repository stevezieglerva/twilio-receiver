from typing import List

from domain.SecurityConcernDTO import SecurityConcernDTO
from domain.IManageSecurityConcerns import IManageSecurityConcerns


class FakeSecurityConcerns(IManageSecurityConcerns):
    def __init__(self):
        pass

    def create_security_concern(
        self,
        name: str,
        created_by_user: str,
    ) -> SecurityConcernDTO:
        pass

    def end_security_concern(
        self,
        security_concern: SecurityConcernDTO,
    ) -> SecurityConcernDTO:
        pass

    def send_alerts_for_open_concerns(self) -> list:
        pass
