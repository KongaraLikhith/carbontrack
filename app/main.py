from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv
import os

from .calculator import UserInputs, calculate_footprint
from .assistant import get_insights

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

# Ensure the static directory exists before mounting
os.makedirs("app/static", exist_ok=True)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
def read_index():
    return FileResponse("app/static/index.html")
