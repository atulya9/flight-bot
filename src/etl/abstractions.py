from abc import ABC, abstractmethod
from typing import Iterable
from src.etl.models import Event, Entity

class Extractor(ABC):
    @abstractmethod
    def extract(self) -> Iterable[Event | Entity]:
        pass

class Transformer(ABC):
    @abstractmethod
    def transform(self, data: Iterable[Event | Entity]) -> Iterable[Event | Entity]:
        pass

class Loader(ABC):
    @abstractmethod
    def load(self, data: Iterable[Event | Entity]) -> None:
        pass
