from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import datetime


class Event(BaseModel):
    event_id: str
    event_type: str
    timestamp: datetime.datetime
    source: str
    payload: Dict[str, Any]


class Entity(BaseModel):
    entity_id: str
    entity_type: str
    source: str
    attributes: Dict[str, Any]


class Airline(BaseModel):
    airline_id: int
    name: str


class Passenger(BaseModel):
    name: str
    seat_number: Optional[str] = None
    class_of_service: Optional[str] = None
    fare: Optional[float] = None
    extras: Optional[str] = None
    loyalty_points: Optional[int] = None
    reward_program_member: Optional[bool] = None


class Flight(BaseModel):
    flight_number: str
    airline_id: int
    departure_datetime: datetime.datetime
    arrival_datetime: datetime.datetime
    departure_time: datetime.time
    arrival_time: datetime.time
    booking_code: str
    status: str
    gate: Optional[str] = None
    terminal: Optional[str] = None
    baggage_claim: Optional[str] = None
    duration_hours: float
    layovers: Optional[int] = None
    layover_locations: Optional[List[str]] = None
    aircraft_type: Optional[str] = None
    pilot: Optional[str] = None
    cabin_crew: Optional[List[str]] = None
    in_flight_entertainment: Optional[bool] = None
    meal_option: Optional[str] = None
    wifi_available: Optional[bool] = None
    window_seat: Optional[bool] = None
    aisle_seat: Optional[bool] = None
    emergency_exit_row: Optional[bool] = None
    number_of_stops: Optional[int] = None
    passenger: Passenger
