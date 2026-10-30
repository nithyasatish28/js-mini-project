from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import functions
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/events")
def get_events(category=None):
    return functions.get_all_events(category=category)

@app.get("/events/{event_id}")
def get_event(event_id: int):
    response = functions.get_event(id=event_id)

    if response is None:
        raise HTTPException(status_code=404, detail="Event not found")

    return response

@app.post("/events")
def add_event(title: str, club: str, category: str, event_date: str, total_seats: int):

    categories = ["technical", "cultural", "sports", "workshop", "seminar"]

    if title.strip() == "" or club.strip() == "":
        raise HTTPException(status_code=422, detail="Fields cannot be empty")

    if category not in categories:
        raise HTTPException(status_code=422, detail="Invalid category")

    if total_seats < 1 or total_seats > 200:
        raise HTTPException(status_code=422, detail="Invalid seat count")

    try:
        datetime.strptime(event_date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=422, detail="Invalid date format")

    return functions.add_event(
        title=title,
        club=club,
        category=category,
        event_date=event_date,
        total_seats=total_seats
    )

@app.delete("/events/{event_id}")
def delete_event(event_id: int):
    response = functions.delete_event(event_id=event_id)

    if response is None:
        raise HTTPException(status_code=404, detail="Event not found")

    if "error" in response:
        raise HTTPException(status_code=409, detail=response["error"])

    return response

@app.post("/events/{event_id}/registrations")
def register_student(event_id: int, roll_no: str):

    if roll_no.strip() == "":
        raise HTTPException(status_code=422, detail="Roll number cannot be empty")

    response = functions.register_student(event_id=event_id, roll_no=roll_no)

    if response is None:
        raise HTTPException(status_code=404, detail="Event not found")

    if "error" in response:
        raise HTTPException(status_code=409, detail=response["error"])

    return response

@app.get("/registrations/{roll_no}")
def get_student_registrations(roll_no: str):
    return functions.get_student_registrations(roll_no=roll_no)


@app.patch("/registrations/{registration_id}/cancel")
def cancel_registration(registration_id: int):

    response = functions.cancel_registration(registration_id=registration_id)

    if response is None:
        raise HTTPException(status_code=404, detail="Registration not found")

    if "error" in response:
        raise HTTPException(status_code=409, detail=response["error"])

    return response
