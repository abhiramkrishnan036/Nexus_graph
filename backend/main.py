from fastapi import FastAPI
from langchain_groq import ChatGroq
import uvicorn

# 1. Initialize the app
app = FastAPI()

# 2. Configure the AI (Using 8B model to avoid 'Rate Limit' errors)
# PASTE YOUR REAL KEY INSIDE THE QUOTES
import os

# This now pulls the key from the server environment instead of the text
llm = ChatGroq(
    temperature=0,
    model="llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY") 
)

# 3. Heartbeat route (This is what the sidebar looks for)
@app.get("/")
def check_status():
    return {"status": "online"}

# 4. Research route
@app.post("/ask")
async def process_query(data: dict):
    user_text = data.get("text", "")
    response = llm.invoke(user_text)
    return {"answer": response.content}

# 5. Start command
if __name__ == "__main__":
    # Get the port from the environment, default to 8000
    port = int(os.environ.get("PORT", 8000))
    # host="0.0.0.0" allows external connections (needed for cloud)
    uvicorn.run(app, host="0.0.0.0", port=port)