from abc import ABC, abstractmethod
from domain.SecurityConcernDTO import SecurityConcernDTO


class IRepository(ABC):
    def __init__(self, source: str):
        self.source = source
        pass

    @abstractmethod
    def get_security_concern(self, id: str) -> SecurityConcernDTO:
        raise NotImplemented

    @abstractmethod
    def save_security_concern(self, security_concern: SecurityConcernDTO) -> dict:
        raise NotImplemented

    @abstractmethod
    def get_open_security_concerns(self) -> list:
        raise NotImplemented

    @abstractmethod
    def delete_security_concern(self, security_concern: SecurityConcernDTO):
        raise NotImplemented
