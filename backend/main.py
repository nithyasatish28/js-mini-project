from fastapi import FastAPI , HTTPException
from fastapi.middleware.cors import CORSMiddleware

import functions

app = FastAPI(
    title = "Campus Event Registration API",
    description="See campus events, register with your roll number and cancel",
)




@app.get("/events")
def events(category=None):
    if category is not None and functions.is_valid_category(category=category) == False:
        raise HTTPException(status_code=422,detail="Category must be technical, cultural, sports, workshop or seminar")
    return functions.get_all_events(category=category)

@app.get("/events/{event_id}")
def event(event_id:int):
    if functions.get_event(id=event_id) is None:
        raise HTTPException(status_code=404,detail="This event is not found")
    return functions.get_event(id=event_id)

@app.post("/events",status_code=201)
def add_event(title , club , category , event_date , total_seats:int):
    if title.strip() == "" or club.strip() == "":
        raise HTTPException(status_code=422,detail="Title and club cannot be empty")
    if functions.is_valid_category(category=category) == False:
        raise HTTPException(status_code=422,detail="Category must be technical, cultural, sports, workshop or seminar")
    if total_seats < 1 or total_seats > 200:
        raise HTTPException(status_code=422,detail="Total seats must be between 1 and 200")
    if functions.is_valid_date(event_date=event_date) == False:
        raise HTTPException(status_code=422,detail="Date must be written as YYYY-MM-DD")
    return functions.add_event(title=title,club=club,category=category,event_date=event_date,total_seats=total_seats)

@app.delete("/events/{event_id}")
def delete_event(event_id:int):
    if functions.get_event(id=event_id) is None:
        raise HTTPException(status_code=404,detail="This event is not found")
    if functions.has_registrations(event_id=event_id) == True:
        raise HTTPException(status_code=409,detail="This event still has registrations")
    functions.delete_event(id=event_id)
    return {"message":"deleted"}

@app.post("/events/{event_id}/registrations",status_code=201)
def register(event_id:int , roll_no):
    event = functions.get_event(id=event_id)
    if event is None:
        raise HTTPException(status_code=404,detail="This event is not found")
    if roll_no.strip() == "":
        raise HTTPException(status_code=422,detail="Roll number cannot be empty")
    if functions.is_past(event_date=event["event_date"]) == True:
        raise HTTPException(status_code=409,detail="This event is already over")
    if functions.is_registered(event_id=event_id,roll_no=roll_no) == True:
        raise HTTPException(status_code=409,detail="You are already registered for this event")
    if event["seats_left"] <= 0:
        raise HTTPException(status_code=409,detail="This event is full.")
    return functions.register(event_id=event_id,roll_no=roll_no)

@app.get("/registrations")
def registrations(roll_no):
    if roll_no.strip() == "":
        raise HTTPException(status_code=422,detail="Roll number cannot be empty")
    return functions.get_student_registrations(roll_no=roll_no)

@app.patch("/registrations/{id}/cancel")
def cancel_registration(id:int):
    registration = functions.get_registration(id=id)
    if registration is None:
        raise HTTPException(status_code=404,detail="This registration is not found")
    if registration["cancelled_on"] is not None:
        raise HTTPException(status_code=409,detail="This registration is already cancelled")
    return functions.cancel_registration(id=id)