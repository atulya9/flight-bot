
"""Configuration for the flight data analysis project."""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Gemini API Key
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# Gemini Model
GEMINI_MODEL = "gemini-2.5-flash"

# Ideal Schemas
IDEAL_FLIGHTS_SCHEMA = {
    "airline_id": "int64",
    "flight_number": "int64",
    "departure_datetime": "datetime64[ns]",
    "arrival_datetime": "datetime64[ns]",
    "booking_status": "object",
    "cabin_class": "object",
    "fare": "float64",
    "loyalty_points": "int64",
    "flight_duration_hours": "float64",
    "is_window_seat": "bool",
    "is_aisle_seat": "bool",
    "is_reward_program_member": "bool",
}

IDEAL_AIRLINES_SCHEMA = {
    "airline_id": "int64",
    "airline_name": "object",
}
