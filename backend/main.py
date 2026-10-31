from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import functions

app = FastAPI(
    title = "Hostel-Complaints-Tracker API",
    description = "Manage Hostel Complaints"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173" , "https://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"]
)

VALID_CATEGORIES = ["electrical", "plumbing", "furniture", "cleaning", "internet"]
VALID_STATUSES = ["open", "in_progress", "resolved"]

@app.get("/complaints")
def get_complaints(status=None, category=None):
    return functions.get_complaints(status=status, category=category)

@app.get("/complaints/stats/counts")
def get_status_counts():
    return functions.get_complaint_status_counts()

@app.get("/complaints/{id}")
def get_one_complaint(id: int):
    result = functions.get_one_complaint(id=id)
    if not result:
        raise HTTPException(status_code=404, detail="Complaint not found")
    return result

@app.post("/complaints")
def create_complaint(rollno: str, roomno: int, description: str, category: str):
    if category not in VALID_CATEGORIES:
        raise HTTPException(status_code=422, detail="Category not in the list.")
        
    if len(description) < 10:
        raise HTTPException(status_code=422, detail="Description must be at least 10 characters.")
        
    return functions.create_complaint(rollno=rollno, roomno=roomno, category=category, description=description)

@app.patch("/complaints/{complaint_id}")
def update_complaint(complaint_id: int, new_status: str, note: str = None):
    if new_status not in VALID_STATUSES:
        raise HTTPException(status_code=422, detail="Invalid status.")
    return functions.update_complaint_status(complaint_id=complaint_id, new_status=new_status, note=note)

@app.get("/complaints/student/{rollno}")
def get_complaints_by_rollno(rollno: str):
    return functions.get_students_complaints_byrollno(rollno=rollno)

@app.delete("/complaints/{id}")
def delete_complaint(id: int):
    return functions.delete_complaint(complaint_id=id)