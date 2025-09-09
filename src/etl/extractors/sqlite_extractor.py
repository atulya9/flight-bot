import sqlite3
from typing import Iterable
from src.etl.abstractions import Extractor
from src.etl.models import Event

class SqliteExtractor(Extractor):
    def __init__(self, db_path: str, table_name: str, source: str):
        self.db_path = db_path
        self.table_name = table_name
        self.source = source

    def extract(self) -> Iterable[Event]:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {self.table_name}")
        for row in cursor.fetchall():
            yield Event(
                event_id=str(row['event_id']),
                event_type=row['event_type'],
                timestamp=row['timestamp'],
                source=self.source,
                payload=dict(row)
            )
        conn.close()
