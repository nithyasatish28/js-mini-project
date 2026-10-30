from fastapi import FastAPI , HTTPException
import functions

app =FastAPI()

@app.get("/events")
def show_events(category=None):
    return functions.get_all_events(category=category)

@app.get("/events/{event_id}")
def event_by_id(event_id):
    return functions.get_all_events(event_id=event_id)

@app.post("/events")
def add_events(title, club, category, date ,total_seats):
    return functions.add_events(title=title ,club=club,category=category,date=date ,total_seats=total_seats)


@app.delete("/events/{event_id}")
def remove_events(event_id):
    return functions.delete_events(event_id=event_id)

@app.post("/events/{event_id}/registrations")
def register_events(event_id: int, roll_no):
    return functions.register(event_id=event_id, roll_no=roll_no)

