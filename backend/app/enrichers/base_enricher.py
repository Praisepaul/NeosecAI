from abc import ABC, abstractmethod


class BaseEnricher(ABC):

    @abstractmethod
    def enrich(self, finding: dict) -> dict:
        pass