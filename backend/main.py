import os, re, json, requests
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

load_dotenv()
app = FastAPI()

# Allow Frontend to connect
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class QueryRequest(BaseModel):
    query: str

@app.post("/recommend")
def recommend(req: QueryRequest):
    # 1. Setup the AI Prompt
    prompt = f"Recommend 5 products for: {req.query}. Return ONLY a JSON list with: name, price, description, link. No extra text."

    # 2. Call Groq API
    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}"},
        json={
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "user", "content": prompt}]
        }
    )
    
    # 3. Handle Errors
    data = response.json()
    if "error" in data: return {"error": data["error"]["message"]}

    # 4. Extract and Parse JSON from AI response
    ai_text = data["choices"][0]["message"]["content"]
    match = re.search(r"\[.*\]", ai_text, re.DOTALL)
    
    return json.loads(match.group()) if match else {"error": "AI parsing failed"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
