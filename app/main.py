from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv
import os

from .calculator import UserInputs, calculate_footprint
from .assistant import get_insights, get_chat_response

load_dotenv()

app = FastAPI(title="Carbon Footprint Platform")

class CalculationResponse(BaseModel):
    footprint: dict
    insights: str

@app.post("/api/calculate", response_model=CalculationResponse)
def calculate_and_get_insights(inputs: UserInputs):
    footprint = calculate_footprint(inputs)
    insights = get_insights(footprint)
    
    return {
        "footprint": footprint.model_dump(),
        "insights": insights
    }

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    history: list[ChatMessage]

class ChatResponse(BaseModel):
    response: str

@app.post("/api/chat", response_model=ChatResponse)
def chat_with_assistant(request: ChatRequest):
    history_dicts = [{"role": msg.role, "content": msg.content} for msg in request.history]
    reply = get_chat_response(request.message, history_dicts)
    return {"response": reply}

# Ensure the static directory exists before mounting
os.makedirs("app/static", exist_ok=True)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
def read_index():
    return FileResponse("app/static/index.html")
