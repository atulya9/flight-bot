
import unittest
from unittest.mock import patch
import pandas as pd
from src.analysis_agent import analyze_question, is_query_safe
from src import config

class TestAnalysisAgent(unittest.TestCase):

    def setUp(self):
        """Set up test data."""
        self.flights_data = {
            'airline_id': [1, 1, 2],
            'flight_number': [101, 102, 201]
        }
        self.airlines_data = {
            'airline_id': [1, 2],
            'airline_name': ['Test Airline 1', 'Test Airline 2']
        }
        self.flights_df = pd.DataFrame(self.flights_data)
        self.airlines_df = pd.DataFrame(self.airlines_data)

    @patch('src.analysis_agent.get_analysis_from_gemini')
    @patch('src.analysis_agent.pd.read_csv')
    def test_analyze_question_safe_query(self, mock_read_csv, mock_get_analysis):
        """Test analyze_question with a safe query."""
        mock_read_csv.side_effect = [self.flights_df, self.airlines_df]
        mock_get_analysis.return_value = {
            'query': "flights_df.merge(airlines_df, on='airline_id')['airline_name'].value_counts().idxmax()",
            'response_template': "The airline with the most flights is {result}."
        }

        result = analyze_question("Which airline has the most flights listed?")
        self.assertEqual(result, "The airline with the most flights is Test Airline 1.")

    def test_is_query_safe(self):
        """Test the is_query_safe function."""
        self.assertTrue(is_query_safe("flights_df.head()"))
        self.assertFalse(is_query_safe("flights_df.to_csv('test.csv')"))
        self.assertFalse(is_query_safe("os.system('rm -rf /')"))
        self.assertFalse(is_query_safe("eval('1+1')"))

if __name__ == '__main__':
    unittest.main()
