from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import date
import functions

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
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
def add_event(title: str, club: str, category: str, event_date:date, total_seats: int):
    if category not in ["technical", "cultural", "sports", "workshop", "seminar"]:
        raise HTTPException(422, "Invalid category")
    if total_seats < 1 or total_seats > 200:
        raise HTTPException(422, "Total seats must be between 1 and 200")
    return functions.add_event(title=title, club=club, category=category, event_date=str(event_date), total_seats=total_seats)

@app.delete("/events/{event_id}")
def delete_event(event_id: int):
    response = functions.delete_event(event_id=event_id)
    if response is None:
        raise HTTPException(status_code=404, detail="Event not found")
    if "error" in response:
        raise HTTPException(status_code=409, detail=response["error"])
    return response


@app.post("/events/{event_id}/registrations")
def register_student(event_id: int, roll_no: int):
    if roll_no <= 0:
        raise HTTPException(422, "Roll number must be more than 0")
    result = functions.register_student(event_id, str(roll_no))
    if result is None:
        raise HTTPException(404, "Event not found")
    if "error" in result:
        raise HTTPException(409, result["error"])
    return result


@app.get("/registrations")
def get_student_registrations(roll_no:int):
    if roll_no <= 0:
        raise HTTPException(422, "Roll number must be more than 0")
    return functions.get_student_registrations(roll_no=roll_no)


@app.patch("/registrations/{registration_id}/cancel")
def cancel_registration(registration_id: int):
    response = functions.cancel_registration(registration_id=registration_id)
    if response is None:
        raise HTTPException(status_code=404, detail="Registration not found")
    if "error" in response:
        raise HTTPException(status_code=409, detail=response["error"])
    return response
