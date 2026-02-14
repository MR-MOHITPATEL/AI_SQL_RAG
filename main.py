from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from agents.schema_agent import SchemaAgent
from agents.sql_agent import SQLAgent
from agents.retriever_agent import RetrieverAgent
from agents.synthesizer_agent import SynthesizerAgent
import uvicorn
import os

app = FastAPI(title="Multi-Agent RAG System")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Agents
schema_agent = SchemaAgent()
sql_agent = SQLAgent()
retriever_agent = RetrieverAgent()
synthesizer_agent = SynthesizerAgent()

class QuestionRequest(BaseModel):
    question: str

@app.get("/")
async def read_root():
    return FileResponse("index.html")

@app.post("/ask")
async def ask_question(request: QuestionRequest):
    question = request.question
    response_data = {
        "question": question,
        "answer": "",
        "schema_used": "",
        "generated_sql": "",
        "rows": [],
        "error": None
    }

    try:
        # 1. Get Schema
        # The agent returns the full schema dictionary
        schema = schema_agent.get_schema(question)
        response_data["schema_used"] = schema

        # 2. Generate SQL
        # 2. Generate SQL
        generated_sql = sql_agent.generate_sql(question, schema)
        
        if generated_sql == "NO_QUERY":
            response_data["answer"] = "Please ask a question related to the database (e.g., 'Show me top customers', 'How many orders were placed last month?')."
            response_data["error"] = "Irrelevant query detected."
            return response_data

        response_data["generated_sql"] = generated_sql

        # 3. Retrieve Data
        retrieval_result = retriever_agent.execute_query(generated_sql)
        
        # Check for DB execution errors
        if retrieval_result.get("error"):
            response_data["error"] = retrieval_result["error"]
            response_data["answer"] = "I encountered an error while executing the database query."
            # We return early but still provide the SQL that failed
            return response_data
        
        rows = retrieval_result["rows"]
        response_data["rows"] = rows

        # 4. Synthesize Answer
        if not rows:
            response_data["answer"] = "No matching records found."
        else:
            answer = synthesizer_agent.synthesize_answer(question, generated_sql, rows, schema)
            response_data["answer"] = answer

    except Exception as e:
        response_data["error"] = str(e)
        response_data["answer"] = "I encountered an error processing your request."
    
    return response_data

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
