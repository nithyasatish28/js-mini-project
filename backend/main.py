from fastapi import FastAPI, HTTPException
import functions

app = FastAPI()


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
def add_event(title, club, category, event_date, total_seats: int):
    return functions.add_event(title=title, club=club, category=category, event_date=event_date, total_seats=total_seats)


@app.delete("/events/{event_id}")
def delete_event(event_id: int):
    response = functions.delete_event(event_id=event_id)
    if response is None:
        raise HTTPException(status_code=404, detail="Event not found")
    if "error" in response:
        raise HTTPException(status_code=409, detail=response["error"])
    return response


@app.post("/events/{event_id}/registrations", status_code=201)
def register_student(event_id: int, roll_no):
    response = functions.register_student(event_id=event_id, roll_no=roll_no)
    if response is None:
        raise HTTPException(status_code=404, detail="Event not found")
    if "error" in response:
        raise HTTPException(status_code=409, detail=response["error"])
    return response


@app.get("/registrations")
def get_student_registrations(roll_no):
    return functions.get_student_registrations(roll_no=roll_no)


@app.patch("/registrations/{registration_id}/cancel")
def cancel_registration(registration_id: int):
    response = functions.cancel_registration(registration_id=registration_id)
    if response is None:
        raise HTTPException(status_code=404, detail="Registration not found")
    if "error" in response:
        raise HTTPException(status_code=409, detail=response["error"])
    return response
