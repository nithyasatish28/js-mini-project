from fastapi import FastAPI ,HTTPException
import function 
app = FastAPI()

@app.get("/Events")
def events():
    return function.get_all_event(  )



@app.get ("/Events")
def events(id):
    return function.get_event(id=id) 


@app.post("/Events")
def events(title: str, club: str, category: str, events_date:str,total_seats:int):
    return function.add_new_event(title=title, club=club, category=category, events_date=events_date ,total_seats=total_seats ,seats_left=total_seats)


@app.delete("/Events")
def events (id):
    return function.delete_event(id=id)