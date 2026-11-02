from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from datetime import date
from typing import Optional
import functions

app = FastAPI(
    title="Campus Event Registration API",
    description="Backend API for managing campus events and student registrations",
    version="1.0.0"
)

# CORS Middleware to allow requests from React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

VALID_CATEGORIES = ["technical", "cultural", "sports", "workshop", "seminar"]


class EventCreate(BaseModel):
    title: str = Field(..., description="Event title")
    club: str = Field(..., description="Organizing club")
    category: str = Field(..., description="Category: technical, cultural, sports, workshop, seminar")
    event_date: str = Field(..., description="Date written as YYYY-MM-DD")
    total_seats: int = Field(..., description="Total seats between 1 and 200")


class RegistrationCreate(BaseModel):
    roll_no: str = Field(..., description="Student roll number")


# E1: GET ALL EVENTS (optional category filter)
@app.get("/events", status_code=200)
def get_events(category: Optional[str] = Query(None)):
    return functions.get_all_events(category=category)


# E2: GET ONE EVENT
@app.get("/events/{event_id}", status_code=200)
def get_event(event_id: int):
    event = functions.get_event(event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


# E3: ADD EVENT
@app.post("/events", status_code=201)
def add_event(event: EventCreate):
    # Rule 7: Check empty title or club
    if not event.title.strip():
        raise HTTPException(status_code=422, detail="Title cannot be empty")
    if not event.club.strip():
        raise HTTPException(status_code=422, detail="Club cannot be empty")

    # Rule 7: Check valid category
    if event.category not in VALID_CATEGORIES:
        raise HTTPException(
            status_code=422,
            detail=f"Invalid category. Must be one of: {', '.join(VALID_CATEGORIES)}"
        )

    # Rule 7: Check total_seats between 1 and 200
    if event.total_seats < 1 or event.total_seats > 200:
        raise HTTPException(status_code=422, detail="Total seats must be between 1 and 200")

    # Rule 7: Check date format is strictly YYYY-MM-DD
    try:
        parsed_date = date.fromisoformat(event.event_date)
        if len(event.event_date) != 10 or parsed_date.isoformat() != event.event_date:
            raise ValueError()
    except Exception:
        raise HTTPException(status_code=422, detail="Date must be written as YYYY-MM-DD")

    return functions.add_event(
        title=event.title.strip(),
        club=event.club.strip(),
        category=event.category,
        event_date=event.event_date,
        total_seats=event.total_seats
    )


# E4: DELETE EVENT
@app.delete("/events/{event_id}", status_code=200)
def delete_event(event_id: int):
    response = functions.delete_event(event_id)
    if response is None:
        raise HTTPException(status_code=404, detail="Event not found")

    if "error" in response:
        # Rule 5: Deleting an event that still has registrations not cancelled
        raise HTTPException(status_code=409, detail=response["error"])

    return response


# E5: REGISTER STUDENT
@app.post("/events/{event_id}/registrations", status_code=201)
def register_student(event_id: int, reg: RegistrationCreate):
    roll_no = reg.roll_no.strip()
    # Rule 7: Roll number cannot be empty
    if not roll_no:
        raise HTTPException(status_code=422, detail="Roll number cannot be empty")

    response = functions.register_student(event_id, roll_no)
    if response is None:
        # Rule 6: Event doesn't exist
        raise HTTPException(status_code=404, detail="Event not found")

    if "error" in response:
        # Rule 1, 2, 3: Full, duplicate, or past event
        raise HTTPException(status_code=409, detail=response["error"])

    return response


# E6: GET STUDENT REGISTRATIONS
@app.get("/registrations/{roll_no}", status_code=200)
def get_student_registrations(roll_no: str):
    return functions.get_student_registrations(roll_no.strip())


# E7: CANCEL REGISTRATION
@app.patch("/registrations/{registration_id}/cancel", status_code=200)
def cancel_registration(registration_id: int):
    response = functions.cancel_registration(registration_id)
    if response is None:
        # Rule 6: Registration doesn't exist
        raise HTTPException(status_code=404, detail="Registration not found")

    if "error" in response:
        # Rule 4: Registration already cancelled
        raise HTTPException(status_code=409, detail=response["error"])

    return response
