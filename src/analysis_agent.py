import pandas as pd
import google.generativeai as genai
import json
from dotenv import load_dotenv
from .config import GEMINI_MODEL, GEMINI_API_KEY

load_dotenv()

# A set of blocked keywords to prevent write operations
BLOCKED_KEYWORDS = {
    ".to_csv",
    ".to_excel",
    ".to_sql",
    ".to_pickle",
    "open(",
    "exec(",
    "os.system",
    "subprocess",
}


def is_query_safe(query: str) -> bool:
    """Checks if the generated query is safe to execute."""
    query_lower = query.lower()
    # eval is blocked, but we are using it, so we need to be careful.
    # We will only allow simple pandas operations.
    if "eval(" in query_lower:
        return False
    for keyword in BLOCKED_KEYWORDS:
        if keyword in query_lower:
            return False
    return True


def get_analysis_from_gemini(
    question: str, flights_df_head: str, airlines_df_head: str
) -> dict:
    """Gets a pandas query and a response template from Gemini."""
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel(GEMINI_MODEL)

    prompt = f"""
    You are a data analysis expert. Given a natural language question and the heads of two pandas DataFrames
    (`flights_df` and `airlines_df`), generate a JSON object with two keys:
    1.  `query`: A pandas query to extract the answer from the DataFrames.
    2.  `response_template`: A natural language string with a placeholder `{{result}}` where the answer should be inserted.

    Natural Language Question:
    {question}

    `flights_df` Head:
    ```
    {flights_df_head}
    ```

    `airlines_df` Head:
    ```
    {airlines_df_head}
    ```

    Example for "Which airline has the most flights listed?":
    {{
        "query": "flights_df.merge(airlines_df, on='airline_id')['airline_name'].value_counts().idxmax()",
        "response_template": "The airline with the most flights is {{result}}."
    }}
    For queries that don't relate to the dataframes, send an appropriate error response.
    example: {{"error: "Response message"}}

    Generate only the JSON object. 
    """

    response = model.generate_content(prompt)
    cleaned_response = response.text.strip().replace("```json", "").replace("```", "")
    return json.loads(cleaned_response)


def analyze_question(question: str):
    """Analyzes a question and returns the answer."""
    try:
        flights_df = pd.read_csv("data/cleaned_flights.csv")
        airlines_df = pd.read_csv("data/cleaned_airlines.csv")
    except FileNotFoundError as e:
        return f"Error reading data files: {e}"

    flights_df_head = flights_df.head().to_string()
    airlines_df_head = airlines_df.head().to_string()

    analysis = get_analysis_from_gemini(question, flights_df_head, airlines_df_head)
    if "error" in analysis:
        return f"Error: {analysis['error']}"

    query = analysis.get("query")
    response_template = analysis.get("response_template")

    print("--- Generated Query ---")
    print(query)
    print("-----------------------")

    if not is_query_safe(query):
        return "Error: The generated query is not allowed for security reasons."

    try:
        # We are using eval here, but the guardrail should prevent malicious code.
        result = eval(
            query, {"flights_df": flights_df, "airlines_df": airlines_df, "pd": pd}
        )
        return response_template.format(result=result)
    except Exception as e:
        return f"Error executing query: {e}"
