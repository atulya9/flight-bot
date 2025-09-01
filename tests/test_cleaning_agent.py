
import os
import unittest
import pandas as pd
from unittest.mock import patch
from src.cleaning_agent import clean_data
from src import config

class TestCleaningAgent(unittest.TestCase):

    def setUp(self):
        """Set up test data."""
        self.test_data_dir = 'tests/data'
        self.flights_file = os.path.join(self.test_data_dir, 'flights.csv')
        self.airlines_file = os.path.join(self.test_data_dir, 'airlines.csv')
        self.cleaned_flights_file = os.path.join(self.test_data_dir, 'cleaned_flights.csv')
        self.cleaned_airlines_file = os.path.join(self.test_data_dir, 'cleaned_airlines.csv')

        # Create dummy data
        flights_data = {
            'airlie_id': [1, 2],
            'flght#': [101, 202],
            'departure_dt': ['2023-01-01 10:00:00', '2023-01-02 14:00:00'],
            'arrival_dt': ['2023-01-01 12:00:00', '2023-01-02 16:00:00'],
            'status': ['Confirmed', 'Cancelled'],
            'class': ['Economy', 'Business'],
            'fare': [250.0, 800.0],
            'loyalty_pts': [100, None],
            'duration_hrs': [2.0, 4.0],
            'window_seat': [True, False],
            'aisle_seat': [False, True],
            'reward_program_member': ['Yes', 'No']
        }
        airlines_data = {
            'airlie_id': [1, 2],
            'airline_name': ['Test Airline 1', 'Test Airline 2']
        }
        pd.DataFrame(flights_data).to_csv(self.flights_file, index=False)
        pd.DataFrame(airlines_data).to_csv(self.airlines_file, index=False)

    def tearDown(self):
        """Clean up test data."""
        for f in [self.flights_file, self.airlines_file, self.cleaned_flights_file, self.cleaned_airlines_file]:
            if os.path.exists(f):
                os.remove(f)

    @patch('src.cleaning_agent.get_column_mapping_from_gemini')
    def test_clean_data(self, mock_get_mapping):
        """Test the clean_data function."""
        # Mock the return value of the gemini api call
        mock_get_mapping.side_effect = [
            {
                'airlie_id': 'airline_id',
                'flght#': 'flight_number',
                'departure_dt': 'departure_datetime',
                'arrival_dt': 'arrival_datetime',
                'status': 'booking_status',
                'class': 'cabin_class',
                'fare': 'fare',
                'loyalty_pts': 'loyalty_points',
                'duration_hrs': 'flight_duration_hours',
                'window_seat': 'is_window_seat',
                'aisle_seat': 'is_aisle_seat',
                'reward_program_member': 'is_reward_program_member'
            },
            {
                'airlie_id': 'airline_id',
                'airline_name': 'airline_name'
            }
        ]

        clean_data(data_dir=self.test_data_dir)

        # Check if cleaned files are created
        self.assertTrue(os.path.exists(self.cleaned_flights_file))
        self.assertTrue(os.path.exists(self.cleaned_airlines_file))

        # Check cleaned flights data
        cleaned_flights_df = pd.read_csv(self.cleaned_flights_file)
        self.assertListEqual(list(cleaned_flights_df.columns), list(config.IDEAL_FLIGHTS_SCHEMA.keys()))
        self.assertEqual(cleaned_flights_df['loyalty_points'].dtype, 'int64')

        # Check cleaned airlines data
        cleaned_airlines_df = pd.read_csv(self.cleaned_airlines_file)
        self.assertListEqual(list(cleaned_airlines_df.columns), list(config.IDEAL_AIRLINES_SCHEMA.keys()))

if __name__ == '__main__':
    unittest.main()
