
# LLM-Powered Flight Data Analysis

This project uses LLM-powered agents to automatically clean and analyze a flight booking dataset.

## Features

- **LLM-Powered Data Cleaning:** Automatically cleans and transforms raw CSV data into a usable format.
- **Natural Language Queries:** Ask questions about the flight data in plain English.
- **Dynamic Query Generation:** Uses an LLM to dynamically generate pandas queries to answer your questions.
- **Safety Guardrails:** Includes a guardrail to prevent the execution of malicious code.

## Setup

1.  **Create a virtual environment:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

2.  **Install dependencies:**
    This project uses `uv` for package management. Install it if you haven't already:
    ```bash
    pip install uv
    ```
    Then, install the project dependencies:
    ```bash
    uv pip sync pyproject.toml
    ```

3.  **Set up your Gemini API Key:**
    Create a `.env` file in the root of the project and add your Gemini API key:
    ```
    GEMINI_API_KEY=your_api_key
    ```

## Usage

### 1. Clean the Data

Before you can analyze the data, you need to clean it. The main script will do this automatically for you the first time you run it. If you add new data to the `data` directory, you can force a cleaning by using the `--clean` flag.

To run the cleaning process explicitly:
```bash
.venv/bin/python src/cleaning_agent.py
```

### 2. Analyze the Data

To ask a question, run the `main.py` script with your question as an argument:

```bash
.venv/bin/python -m src.main "Your question here"
```

**Example Questions:**

-   `"Which airline has the most flights listed?"`
-   `"What are the top three most frequented destinations?"` (Note: This is not implemented yet as the destination column is not in the ideal schema)
-   `"Number of bookings for American Airlines yesterday."` (Note: This is not implemented yet)

**Force cleaning and then analyze:**
```bash
.venv/bin/python -m src.main "Which airline has the most flights listed?" --clean
```

## Running Tests

To run the unit tests, use the following command:

```bash
.venv/bin/python -m unittest discover tests
```
