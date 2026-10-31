
from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
import function

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://127.0.0.1:8000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------- Events ----------

@app.get("/events")
def get_events(category=None):
    return function.get_events(category=category)


@app.get("/events/{event_id}")
def get_event(event_id: int):
    event = function.get_event(event_id)

    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    return event


@app.post("/events", status_code=201)
def add_event(title: str, club: str, category: str,
              event_date: str, total_seats: int):

    if total_seats < 1 or total_seats > 200:
        raise HTTPException(status_code=422, detail="Seats must be between 1 and 200")

    if category not in ["technical", "cultural", "sports", "workshop", "seminar"]:
        raise HTTPException(status_code=422, detail="Invalid category")

    data = {
        "title": title,
        "club": club,
        "category": category,
        "event_date": event_date,
        "total_seats": total_seats
    }

    return function.add_event(data)


@app.delete("/events/{event_id}", status_code=204)
def delete_event(event_id: int):
    result = function.delete_event(event_id)

    if result == "not_found":
        raise HTTPException(status_code=404, detail="Event not found")

    if result == "registered":
        raise HTTPException(status_code=409, detail="Students are registered for this event")

    return Response(status_code=204)




@app.post("/events/{event_id}/register", status_code=201)
def register_student(event_id: int, roll_no: str):

    result = function.register_student(event_id, roll_no)

    if result == "not_found":
        raise HTTPException(status_code=404, detail="Event not found")

    if result == "past_event":
        raise HTTPException(status_code=409, detail="Event date has passed")

    if result == "full":
        raise HTTPException(status_code=409, detail="No seats available")

    if result == "already_registered":
        raise HTTPException(status_code=409, detail="Already registered")

    return {"message": "Registered successfully"}


@app.get("/students/{roll_no}/registrations")
def get_student_events(roll_no: str):
    return function.get_student_registrations(roll_no)


@app.patch("/registrations/{registration_id}/cancel")
def cancel_registration(registration_id: int):

    result = function.cancel_registration(registration_id)

    if result == "not_found":
        raise HTTPException(status_code=404, detail="Registration not found")

    if result == "already_cancelled":
        raise HTTPException(status_code=409, detail="Already cancelled")

    return {"message": "Registration cancelled successfully"}
