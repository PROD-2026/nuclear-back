from abc import ABC, abstractmethod

from src.domain.vaule_objects.vulnerability import VulnerabilityMLInfo


class IMLProvider(ABC):
    @abstractmethod
    async def check_vulnerabilities(
        self, values: list[str]
    ) -> list[VulnerabilityMLInfo]:
        raise NotImplementedError

    @abstractmethod
    async def get_recommendations(self) -> ...:  # TODO!
        raise NotImplementedError
