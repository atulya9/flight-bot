import json
import google.generativeai as genai
from src import config
from pydantic import BaseModel

class SchemaMapper:
    def __init__(self, model_name: str = config.GEMINI_MODEL):
        genai.configure(api_key=config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(model_name)

    def get_schema_mapping(self, source_columns: list[str], target_schema: BaseModel) -> dict:
        """Gets column mapping from Gemini API.

        Args:
            source_columns: A list of raw column names from the source data.
            target_schema: A Pydantic model representing the target schema.

        Returns:
            A dictionary mapping raw column names to target column names.
        """
        prompt = f"""
        You are a data mapping expert. Given a list of raw column names and a target Pydantic schema,
        generate a JSON object that maps the raw column names to the target schema's field names.

        The raw column names are similar to the target schema, but may contain human error like typos.
        Your job is to identify which raw column should be mapped to which target column.

        Generate only the JSON object mapping raw columns to target columns.
        Ensure that all columns in the target schema are present as values in the JSON object.
        Example format: {{"raw_coln_1": "target_column_1", "col_2": "target_column_2"}}

        Raw Columns:
        ```python
        source_columns = {source_columns}
        ```

        Target Schema:
        ```python
        target_schema = {list(target_schema.model_fields.keys())}
        ```
        """

        response = self.model.generate_content(prompt)
        # Clean the response to extract only the JSON part
        cleaned_response = response.text.strip().replace("```json", "").replace("```", "")
        return json.loads(cleaned_response)
