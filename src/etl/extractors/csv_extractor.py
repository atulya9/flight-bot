import pandas as pd
from typing import Iterable
from src.etl.abstractions import Extractor
from src.etl.models import Event, Entity


class CsvExtractor(Extractor):
    def __init__(self, file_path: str, source: str):
        self.file_path = file_path
        self.source = source

    def extract(self) -> Iterable[Event | Entity]:
        df = pd.read_csv(self.file_path)
        if 'airline' in self.file_path:
            for _, row in df.iterrows():
                yield Entity(
                    entity_id=str(row['airlie_id']),
                    entity_type='airline',
                    source=self.source,
                    attributes=row.to_dict()
                )
        elif 'flight' in self.file_path:
            for _, row in df.iterrows():
                yield Event(
                    event_id=str(row['flght#']),
                    event_type='flight',
                    timestamp=pd.to_datetime(row['departure_dt']),
                    source=self.source,
                    payload=row.to_dict()
                )
