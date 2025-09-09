"""Main module for the flight data analysis CLI."""
# import argparse
# import os
# from .analysis_agent import analyze_question
# from .cleaning_agent import clean_data


# def main() -> None:
#     """Main function to run the analysis CLI."""
#     parser = argparse.ArgumentParser(description="Ask questions about flight data.")
#     parser.add_argument(
#         "question", type=str, help="The natural language question to ask."
#     )
#     parser.add_argument("--clean", action="store_true", help="Force clean the data.")
#     args = parser.parse_args()

#     # Check if the data is cleaned
#     if (
#         args.clean
#         or not os.path.exists("data/cleaned_flights.csv")
#         or not os.path.exists("data/cleaned_airlines.csv")
#     ):
#         print("\n--- Data Cleaning Process ---")
#         clean_data()
#         print("--- Data Cleaning Complete ---\n")

#     print(f"\n--- Analyzing your question: {args.question} ---")
#     answer = analyze_question(args.question)
#     print("\n--- Answer ---")
#     print(answer)
#     print("--------------")


from src.etl.pipeline import Pipeline
from src.etl.extractors.csv_extractor import CsvExtractor
from src.etl.transformers.ontology_transformer import OntologyTransformer
from src.etl.loaders.sqlite_loader import SqliteLoader
from src.etl.schema_mapper import SchemaMapper

def main():
    # Create instances of the ETL components
    schema_mapper = SchemaMapper()
    ontology_transformer = OntologyTransformer(schema_mapper)
    sqlite_loader = SqliteLoader(db_path="data/warehouse.db")

    # Create and run the airlines pipeline
    airlines_extractor = CsvExtractor(file_path="data/airlines.csv", source="csv")
    airlines_pipeline = Pipeline(airlines_extractor, ontology_transformer, sqlite_loader)
    airlines_pipeline.run()

    # Create and run the flights pipeline
    flights_extractor = CsvExtractor(file_path="data/flights.csv", source="csv")
    flights_pipeline = Pipeline(flights_extractor, ontology_transformer, sqlite_loader)
    flights_pipeline.run()

if __name__ == "__main__":
    main()
