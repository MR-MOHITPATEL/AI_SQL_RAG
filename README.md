# Multi-Agent RAG System

This project implements a Multi-Agent RAG (Retrieval-Augmented Generation) system for natural language querying of a PostgreSQL database. It uses FastAPI for the backend, Google Gemini for SQL generation and answer synthesis, and Faker for generating synthetic data.

## Features

- **Natural Language to SQL**: Converts English questions into efficient SQL queries.
- **Multi-Agent Architecture**:
  - **Schema Agent**: Understands the database structure.
  - **SQL Agent**: Generates SQL queries using OpenAI.
  - **Retriever Agent**: Executes queries safely.
  - **Synthesizer Agent**: Formats the results into a human-readable answer.
- **FastAPI Backend**: Robust API with modular structure.
- **Synthetic Data**: Script to populate the database with realistic test data.
- **Simple Frontend**: HTML interface to test queries.

## Prerequisites

- Python 3.10+
- PostgreSQL Database installed and running.
- Google Gemini API Key.

## Setup Instructions

1.  **Clone/Open the project** in your terminal.

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Environment Setup**:
    - Copy `.env.example` to `.env`:
        ```bash
        cp .env.example .env
        # On Windows Command Prompt: copy .env.example .env
        ```
    - Open `.env` and fill in your details:
        - `DB_HOST`, `DB_NAME`, `DB_USER`, `DB_PASS` (Make sure the database `DB_NAME` exists in Postgres, e.g., created via `createdb rag_db`).
        - `GEMINI_API_KEY` (Your Google Gemini API Key).

4.  **Database Initialization**:
    - Run the setup script to create tables:
        ```bash
        python database_setup.py
        ```
    - Run the data generator to populate it with synthetic data:
        ```bash
        python data_generator.py
        ```

## Running the Application

1.  **Start the Server**:
    ```bash
    uvicorn main:app --reload
    ```
    The API will be available at `http://localhost:8000`.

2.  **Use the Frontend**:
    - Open `index.html` in your web browser.
    - Type a question (e.g., "How many customers are from New York?") and click "Ask Question".

## API Usage

**Endpoint**: `POST /ask`

**Request Body**:
```json
{
  "question": "Show me the top 5 projects by budget"
}
```

**Response**:
```json
{
  "question": "Show me the top 5 projects by budget",
  "answer": "The top 5 projects by budget are...",
  "schema_used": { ... },
  "generated_sql": "SELECT ...",
  "rows": [ ... ],
  "error": null
}
```

## Architecture

The system follows a pipeline approach:
1.  **User Query** -> **Schema Agent** (Attributes relevant schema info)
2.  **Schema + Query** -> **SQL Agent** (Generates SQL via LLM)
3.  **SQL** -> **Retriever Agent** (Executes on DB)
4.  **Results + Query** -> **Synthesizer Agent** (Generates final answer via LLM)

## Testing

Run the included test script (requires the server to be running):
```bash
pytest test_api.py
```
