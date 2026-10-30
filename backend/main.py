
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import functions

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class Event(BaseModel):
    title: str
    club: str
    category: str
    event_date: str
    total_seats: int

class Registration(BaseModel):
    roll_no: str

@app.get("/events")
def get_events(category=None):

    if category != None:
        if category not in ["technical", "cultural", "sports", "workshop", "seminar"]:
            raise HTTPException(status_code=422, detail="Invalid category")

    return functions.get_all_events(category=category)


