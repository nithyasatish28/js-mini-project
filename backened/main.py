from fastapi import FastAPI ,HTTPException

import function
from datetime import datetime
app = FastAPI(
    title="event tracker API"
)

@app.get("/events")
def get_all_events(category=None):
    if category == "":
        category = None
    return function.get_all_event(category=category )

@app.get ("/events/{event_id}")
def get_event(event_id:int):
    return function.get_event(id=event_id) 


@app.post("/events")
def create_new_event(title: str, club: str, category: str, event_date:str,total_seats:int, seats_left:int):
    if total_seats <=0:
        raise HTTPException(status_code=422,detail="Inavid no of seats" )
    return function.add_new_event(title=title, club=club, category=category, event_date=event_date ,total_seats=total_seats ,seats_left=seats_left)

@app.delete("/events/{event_id}")
def delete_event(event_id:int):
    return function.delete_event(id=event_id)

@app.post("/events/{event_id}/register/{roll_number}")
def event_roll_number(event_id:int , roll_number:int):
    return function.event_roll_number(event_id=event_id , roll_number=roll_number)

@app.get("/events")
def create_event(title: str, club: str, category: str, event_date: int, total_seats: int)
    return function.create_event(
        title =title,
        club =club,
        category=category,
        event_date=event_date,
        total_Seats=total_seats,
    )

@app.patch("/events/{events_id}")
def get_event(event_id: int):
    return function.get_event(event_id=event_id)
    