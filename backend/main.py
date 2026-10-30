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
    complaint = functions.get_complaint(id)
    if complaint is None:
        raise HTTPException(status_code=404, detail="Complaint not found")
    return complaint

#E3
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

    return functions.create_complaint(rollno=rollno, roomno=roomno, category=category, description=description)

#E4
@app.patch("/complaints/{complaint_id}/status")
def update_complaint(complaint_id: int, note: str):
    complaint = functions.get_complaint(complaint_id)
    if complaint is None:
        raise HTTPException(status_code=404, detail="Complaint is not there")
    if complaint["status"] == "resolved":
        raise HTTPException(status_code=409, detail="Resolved complaint can't be changed")
    if note == "":
        raise HTTPException(status_code=422, detail="Can't be empty")
    return functions.update_complaint(complaint_id, note)

#E5
@app.get("/students/{roll_no}/complaints")
def student_complaints(roll_no: str):
    return functions.fetch_student_complaint(roll_no)


#E6
@app.delete("/complaints/{complaint_id}", status_code=204)
def delete_complaint(complaint_id: int):
    complaint = functions.get_complaint(complaint_id)
    if complaint is None:
        raise HTTPException(status_code=404, detail="Complaint not found")
    if complaint["status"] != "open":
        raise HTTPException(status_code=409, detail="Only an open complaint can be deleted")
    functions.remove_complaint(complaint_id)
    return {"message": "Complaint deleted successfully"}


#E7
@app.get("/stats")
def status_counts():
    return functions.get_status_counts()