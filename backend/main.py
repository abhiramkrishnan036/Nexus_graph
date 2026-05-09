import os
from fastapi import FastAPI
from langchain_groq import ChatGroq
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

# 1. Initialize the app
app = FastAPI()

# 2. Unlock CORS so Streamlit can talk to us
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Configure the AI (Ensure your GROQ_API_KEY is in Render Environment Variables!)
llm = ChatGroq(
    temperature=0,
    model="llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY")
)

# 4. Heartbeat route (This MUST work for the light to turn green)
@app.get("/")
def check_status():
    return {"status": "online"}

# 5. Research route
@app.post("/ask")
async def process_query(data: dict):
    user_text = data.get("text", "")
    try:
        response = llm.invoke(user_text)
        return {"answer": response.content}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    # Render uses the PORT environment variable
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)