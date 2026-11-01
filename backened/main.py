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