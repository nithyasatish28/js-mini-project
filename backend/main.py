
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

@app.get("/events/{event_id}")
def get_event(event_id: int):

    response = functions.get_event(id=event_id)

    if response is None:
        raise HTTPException(status_code=404, detail="Event not found")

    return response

@app.post("/events", status_code=201)
def add_event(event: Event):

    if event.title == "" or event.club == "":
        raise HTTPException(status_code=422, detail="Title and club cannot be empty")

    if event.category not in ["technical", "cultural", "sports", "workshop", "seminar"]:
        raise HTTPException(status_code=422, detail="Invalid category")

    if event.total_seats <= 0 or event.total_seats > 200:
        raise HTTPException(status_code=422, detail="Invalid total seats")

    try:
        datetime.strptime(event.event_date, "%Y-%m-%d")
    except:
        raise HTTPException(status_code=422, detail="Invalid date")

    response = functions.add_event(
        title=event.title,
        club=event.club,
        category=event.category,
        event_date=event.event_date,
        total_seats=event.total_seats
    )

    return response
    )

@app.delete("/events/{event_id}")
def delete_event(event_id: int):

    response = functions.delete_event(event_id=event_id)

    if response is None:
        raise HTTPException(status_code=404, detail="Event not found")

    if "error" in response:
        raise HTTPException(status_code=409, detail=response["error"])

    return response


@app.post("/events/{event_id}/registrations", status_code=201)
def register_student(event_id: int, registration: Registration):

    if registration.roll_no.strip() == "":
        raise HTTPException(status_code=422, detail="Roll number cannot be empty")

    response = functions.register_student(
        event_id=event_id,
        roll_no=registration.roll_no
    )

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



