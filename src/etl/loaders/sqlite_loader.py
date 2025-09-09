from typing import Iterable
from sqlalchemy import (
    create_engine,
    Table,
    Column,
    String,
    MetaData,
    DateTime,
    JSON,
    Integer,
    Float,
    Boolean,
)
from src.etl.abstractions import Loader
from src.etl.models import Event, Entity, Airline, Flight


class SqliteLoader(Loader):
    def __init__(self, db_path: str):
        self.engine = create_engine(f"sqlite:///{db_path}")
        self.metadata = MetaData()
        self.airlines_table = self._create_airlines_table()
        self.flights_table = self._create_flights_table()
        self.metadata.create_all(self.engine)

    def _create_airlines_table(self) -> Table:
        return Table(
            "airlines",
            self.metadata,
            Column("airline_id", Integer, primary_key=True),
            Column("name", String),
        )

    def _create_flights_table(self) -> Table:
        return Table(
            "flights",
            self.metadata,
            Column("flight_number", String, primary_key=True),
            Column("airline_id", Integer),
            Column("departure_datetime", DateTime),
            Column("arrival_datetime", DateTime),
            Column("departure_time", DateTime),
            Column("arrival_time", DateTime),
            Column("booking_code", String),
            Column("status", String),
            Column("gate", String),
            Column("terminal", String),
            Column("baggage_claim", String),
            Column("duration_hours", Float),
            Column("layovers", Integer),
            Column("layover_locations", JSON),
            Column("aircraft_type", String),
            Column("pilot", String),
            Column("cabin_crew", JSON),
            Column("in_flight_entertainment", Boolean),
            Column("meal_option", String),
            Column("wifi_available", Boolean),
            Column("window_seat", Boolean),
            Column("aisle_seat", Boolean),
            Column("emergency_exit_row", Boolean),
            Column("number_of_stops", Integer),
            Column("passenger", JSON),
        )

    def load(self, data: Iterable[Event | Entity | Airline | Flight]) -> None:
        with self.engine.connect() as connection:
            for item in data:
                if isinstance(item, Airline):
                    stmt = self.airlines_table.insert().values(**item.dict())
                    connection.execute(stmt)
                elif isinstance(item, Flight):
                    stmt = self.flights_table.insert().values(**item.dict())
                    connection.execute(stmt)
            connection.commit()
