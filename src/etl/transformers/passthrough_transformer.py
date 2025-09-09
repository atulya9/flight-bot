from typing import Iterable
from src.etl.abstractions import Transformer
from src.etl.models import Event, Entity

class PassthroughTransformer(Transformer):
    def transform(self, data: Iterable[Event | Entity]) -> Iterable[Event | Entity]:
        for item in data:
            yield item
