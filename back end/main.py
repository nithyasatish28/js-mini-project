from fastapi import FastAPI,HTTPException
from datetime import datetime
import functions

app = FastAPI()

@app.get("/events")

@app.post("/events")
def item():
    return functions.add_event(title="Test Event", club="Test Club", category="Test Category", event_date=datetime.now(), total_seats=100)
app = FastAPI()
