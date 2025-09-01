"""Module for cleaning flight and airline data."""

import os
import json
import pandas as pd
import google.generativeai as genai
from src import config

def get_column_mapping_from_gemini(raw_columns: list[str], ideal_schema: dict) -> dict:
    """Gets column mapping from Gemini API.

    Args:
        raw_columns: A list of raw column names from the DataFrame.
        ideal_schema: A dictionary representing the ideal schema with column names and dtypes.

    Returns:
        A dictionary mapping raw column names to ideal column names.
    """
    genai.configure(api_key=config.GEMINI_API_KEY)
    model = genai.GenerativeModel(config.GEMINI_MODEL)

    prompt = f"""
    You are a data mapping expert. Given a list of raw column names and an target schema,
    generate a JSON object that maps the raw column names to the target column names.

    The raw column names are similar to the target schema, but may contain human error like typos. 
    Your job is to identify which raw column should be mapped to which target column.

    Generate only the JSON object mapping raw columns to target columns.
    Ensure that all columns in the target schema are present as values in the JSON object.
    Example format: {{\"raw_coln_1\": \"target_column_1\", \"col_2\": \"target_column_2\"}}

    Raw Columns:
    ```python
    raw_columns = {raw_columns}
    ```

    target Schema:
    ```python
    target_columns = {list(ideal_schema.keys())}
    ```
    """

    response = model.generate_content(prompt)
    # Clean the response to extract only the JSON part
    cleaned_response = response.text.strip().replace("```json", "").replace("```", "")
    return json.loads(cleaned_response)

def clean_data(data_dir: str = 'data') -> None:
    """Reads, cleans, and saves flight and airline data.

    Args:
        data_dir: The directory where raw and cleaned data files are stored.
    """
    print("\n--- Cleaning Flights Data ---")
    try:
        df = pd.read_csv(os.path.join(data_dir, 'flights.csv'))
    except FileNotFoundError as e:
        print(f"Error reading flights data file: {e}")
        return

    ideal_schema = config.IDEAL_FLIGHTS_SCHEMA

    raw_columns = df.columns.tolist()
    column_mapping = get_column_mapping_from_gemini(raw_columns, ideal_schema)

    print(f"Generated Column Mapping: {column_mapping}")

    df.rename(columns=column_mapping, inplace=True)

    # Keep only the columns from the ideal schema
    df = df[list(ideal_schema.keys())]

    # Handle missing values (simple fillna for now)
    for col in df.columns:
        if df[col].dtype == "float64":
            df[col] = df[col].fillna(df[col].mean())
        elif df[col].dtype == "int64":
            df[col] = df[col].fillna(df[col].median()).astype('int64')
        else:
            df[col] = df[col].fillna("Unknown")

    print("Missing values handled.")

    # Correct data types
    for col, dtype in ideal_schema.items():
        if dtype == "datetime64[ns]":
            df[col] = pd.to_datetime(df[col], errors="coerce")
        elif dtype == "bool":
            df[col] = df[col].apply(lambda x: str(x).lower() in ["true", "yes"])
        else:
            df[col] = df[col].astype(dtype, errors="ignore")

    print("Data types corrected.")

    # Save the cleaned data
    df.to_csv(os.path.join(data_dir, 'cleaned_flights.csv'), index=False)
    print(f"Cleaned flights data saved to {os.path.join(data_dir, 'cleaned_flights.csv')}")

    print("\n--- Cleaning Airlines Data ---")
    try:
        airlines_df = pd.read_csv(os.path.join(data_dir, 'airlines.csv'))
    except FileNotFoundError as e:
        print(f"Error reading airlines data file: {e}")
        return

    ideal_airlines_schema = config.IDEAL_AIRLINES_SCHEMA

    raw_airlines_columns = airlines_df.columns.tolist()
    airlines_column_mapping = get_column_mapping_from_gemini(
        raw_airlines_columns, ideal_airlines_schema
    )

    print(f"Generated Airlines Column Mapping: {airlines_column_mapping}")

    airlines_df.rename(columns=airlines_column_mapping, inplace=True)
    airlines_df = airlines_df[list(ideal_airlines_schema.keys())]

    # Save the cleaned data
    airlines_df.to_csv(os.path.join(data_dir, 'cleaned_airlines.csv'), index=False)
    print(f"Cleaned airlines data saved to {os.path.join(data_dir, 'cleaned_airlines.csv')}")


if __name__ == "__main__":
    clean_data()
