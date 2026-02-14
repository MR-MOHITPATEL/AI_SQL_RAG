import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class SynthesizerAgent:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")
            
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    def synthesize_answer(self, query: str, sql: str, results: list, schema: dict) -> str:
        """
        Synthesizes a human-readable answer from the query results.
        """
        if not results:
            return "Unless I missed something, I couldn't find any matching records for your query."

        # Limit results context to avoid token limits for very large result sets
        results_str = str(results[:50]) # Simple truncation
        if len(results) > 50:
            results_str += f"\n... (and {len(results) - 50} more rows)"

        system_prompt = f"""
        You are a helpful data assistant.
        Your task is to answer the user's question based ONLY on the provided database query results.
        
        Question: {query}
        SQL Used: {sql}
        Results: {results_str}
        
        Rules:
        1. Provide a concise, clear answer.
        2. If the result is a single number or value, state it clearly.
        3. If the result is a list, summarize it (e.g., "The top 3 customers are X, Y, Z").
        4. If the results are empty, politely state that no data was found.
        5. Do not mention "ID" values unless explicitly asked or necessary for distinction.
        """

        try:
            response = self.model.generate_content(system_prompt)
            return response.text.strip()
            
        except Exception as e:
            return f"Error synthesizing answer: {str(e)}"
