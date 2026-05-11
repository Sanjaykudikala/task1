import os
import re
import json
import requests
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Allow all origins (for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str

@app.post("/recommend")
async def recommend(req: QueryRequest):
    query = req.query.strip()
    if not query:
        return {"error": "Query is required"}

    prompt = f"""You are a product recommendation assistant.

Based on the user's query, recommend 5 relevant products.

Return ONLY valid JSON in this format:

[
  {{
    "name": "",
    "price": "",
    "description": "",
    "link": ""
  }}
]

Do not include explanations.
Do not include markdown.
Return only JSON.

User Query:
"{query}"
"""

    headers = {
        "Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}",
        "Content-Type": "application/json",
    }
    body = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}],
    }
    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers=headers,
        json=body,
    )
    data = response.json()
    if "error" in data:
        return {"error": data["error"].get("message", "Groq API error")}
    ai_text = data["choices"][0]["message"]["content"]
    match = re.search(r"\[.*\]", ai_text, re.DOTALL)
    if not match:
        return {"error": "Failed to parse AI response"}
    products = json.loads(match.group())
    return products

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
