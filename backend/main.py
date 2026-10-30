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

#E1
@app.get("/complaints")
def all_complaints():
    return functions.get_all_complaints()

#E2
@app.get("/complaints/{id}")
def get_complaint(id: int):
    complaint = functions.get_complaint(id=id)
    if complaint is None:
        raise HTTPException(status_code=404, detail="Complaint not found")
    return complaint

#3
@app.post("/complaints")
def create_complaint(rollno: str, roomno: str, category: str, description: str):
    
    if rollno == "" or roomno == "" or category == "" or description == "":
        raise HTTPException(status_code=422, detail="Every field has to be filled")
    
    if len(description) <= 9:
        raise HTTPException(status_code=422, detail="Has to be at least 10 characters")
    
    valid = False
    for name in functions.CATEGORIES:
        if name == category:
            valid = True
    if valid == False:
        raise HTTPException(status_code=422, detail="Invalid Category")

    
    for exist in functions.get_all_complaints():
        if exist["room_no"] == roomno:
            if exist["category"] == category:
                if exist["status"] != "resolved":
                    raise HTTPException(status_code=409, detail="Has an unresolved complaint in this category")

    return functions.create_complaint(roll_no=rollno, room_no=roomno, category=category, description=description)