from fastapi import FastAPI ,HTTPException
import function 
app = FastAPI()

@app.get("/")
def root():
    return {}


@app.get("/events")
def get_all_events(category:str=None):
    return function.get_all_event(category=category )



@app.get ("/events/{event_id}")
def get_event(event_id:int):
    return function.get_event(id=event_id) 


@app.post("/events")
def create_new_event(title: str, club: str, category: str, events_date:str,total_seats:int):
    return function.add_new_event(title=title, club=club, category=category, events_date=events_date ,total_seats=total_seats ,seats_left=total_seats)


@app.delete("/events/{event_id}")
def delete_event(event_id:int):
    return function.delete_event(id=event_id)