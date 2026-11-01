from fastapi import FastAPI ,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import functions

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://localhost:5174","http://localhost:5175"],
    allow_methods=["*"],
    allow_headers=["*"]  
)
class EventCreate(BaseModel):
    title:str
    club:str
    category:str
    event_date:str
    total_seats:int

class RegistrationCreate(BaseModel):
    roll_no:str


@app.get("/events")
def get_events(category:str = None):
    return functions.get_all_events(category)

@app.get("/events/{event_id}")
def get_event(event_id:int):
    event = functions.get_event(event_id)

    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@app.post("/events")
def add_event(data:EventCreate):
    return functions.add_event(
        title=data.title,
        club=data.club,
        category=data.category,
        event_date=data.event_date,
        total_seats=data.total_seats
    )

@app.delete("/events/{event_id}")
def delete_event(event_id:int):
    result = functions.delete_event(event_id)
    if result == False:
        raise HTTPException(status_code=404, detail="Event not found")
    return "Event deleted"

@app.post("/events/{event_id}/registrations")
def register(event_id:int,data:RegistrationCreate):
    result = functions.register_event(event_id,data.roll_no)
    if result != "Registration successful":
        raise HTTPException(status_code=409,detail=result)
    return "Registration successful"

@app.get("/registrations/{roll_no}")
def my_registrations(roll_no:str):
    return functions.get_student_registrations(roll_no)

@app.patch("/registrations/{registration_id}/cancel")
def cancel(registration_id:int):
    result = functions.cancel_registration(registration_id)
    if result == False:
        raise HTTPException(status_code = 404, detail="Registration not found")
    return "Registration cancelled"


    
