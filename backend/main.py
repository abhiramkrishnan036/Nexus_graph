import os
from fastapi import FastAPI
from langchain_groq import ChatGroq
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

# 1. Initialize the app
app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

# This allows your Streamlit frontend to talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)
   # 2. Configure the AI
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