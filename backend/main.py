from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import functions

app = FastAPI(
    title = "Hostel Complaint Tracker API"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods = ["*"],
    allow_headers = ["*"],
)

# shows all complaints
@app.get("/complaints")
def complaints():
    return functions.get_all_complaints()

# one complaint based on complaint id, with its updates
@app.get("/complaints/{complaint_id}")
def complaint(complaint_id: int):
    result = functions.get_complaint_by_id(complaint_id=complaint_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Complaint doesn't exist")
    return result

# raises complaint 
@app.post("/complaints")
def add_complaint(roll_no, room_no, category, description):
    return functions.add_new_complaint(roll_no=roll_no, room_no=room_no, category=category, description=description)