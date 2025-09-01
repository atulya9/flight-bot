"""Main module for the flight data analysis CLI."""

import argparse
import os
from .analysis_agent import analyze_question
from .cleaning_agent import clean_data


def main() -> None:
    """Main function to run the analysis CLI."""
    parser = argparse.ArgumentParser(description="Ask questions about flight data.")
    parser.add_argument(
        "question", type=str, help="The natural language question to ask."
    )
    parser.add_argument("--clean", action="store_true", help="Force clean the data.")
    args = parser.parse_args()

    # Check if the data is cleaned
    if (
        args.clean
        or not os.path.exists("data/cleaned_flights.csv")
        or not os.path.exists("data/cleaned_airlines.csv")
    ):
        print("\n--- Data Cleaning Process ---")
        clean_data()
        print("--- Data Cleaning Complete ---\n")

    print(f"\n--- Analyzing your question: {args.question} ---")
    answer = analyze_question(args.question)
    print("\n--- Answer ---")
    print(answer)
    print("--------------")


if __name__ == "__main__":
    main()
