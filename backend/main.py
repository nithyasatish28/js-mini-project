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

# E1: shows all complaints
@app.get("/complaints")
def all_complaints():
    return functions.get_all_complaints()

# E2: one complaint based on complaint id, with its updates
@app.get("/complaints/{complaint_id}")
def complaint_by_id(complaint_id: int):
    result = functions.get_complaint_by_id(complaint_id=complaint_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Complaint doesn't exist")
    return result

# E3: raise a complaint
@app.post("/complaints")
def add_complaint(roll_no, room_no, category, description):
    category = category.lower() # added this because whenever any category with caps was put in, the invalid category error came up
    if roll_no == "" or room_no == "" or category == "" or description == "":
        raise HTTPException(status_code=422, detail="Every field must be filled in")

    valid = False
    for name in functions.Categories:
        if name == category:
            valid = True
    if valid == False:
        raise HTTPException(status_code=422, detail="Invalid Category")

    letters = 0
    for letter in description:
        letters += 1
    if letters <= 9:
        raise HTTPException(status_code=422, detail="Must be at least 10 characters")

    for existing in functions.get_all_complaints():
        if existing["room_no"] == room_no:
            if existing["category"] == category:
                if existing["status"] != "resolved":
                    raise HTTPException(status_code=409, detail="Already has an unresolved complaint in this category")

    return functions.add_new_complaint(roll_no=roll_no, room_no=room_no, category=category, description=description)

# E4: move to the next status, with a note
@app.patch("/complaints/{complaint_id}")
def update_complaint(complaint_id: int, note):
    result = functions.get_complaint_by_id(complaint_id=complaint_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Complaint doesn't exist")
    if result["status"] == "resolved":
        raise HTTPException(status_code=409, detail="Resolved complaint can't be changed")
    if note == "":
        raise HTTPException(status_code=422, detail="Can't be empty")
    return functions.update_complaint(complaint_id=complaint_id, note=note)

# E5: students complaint by roll no
@app.get("/students/{roll_no}/complaints")
def student_complaints(roll_no):
    return functions.fetch_student_complaint(roll_no=roll_no)

# E6: delete but only if still open)
@app.delete("/complaints/{complaint_id}")
def remove_complaint(complaint_id: int):
    result = functions.get_complaint_by_id(complaint_id=complaint_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Complaint doesn't exist")
    if result["status"] is not "open":
        raise HTTPException(status_code=409, detail="Only open complaints can be deleted")
    functions.remove_complaint(complaint_id=complaint_id)
    return {"message": "Complaint deleted"}

# E7: how many complaints in each status
@app.get("/counts")
def counts():
    result = {"open": 0, "in_progress": 0, "resolved": 0}
    for complaint in functions.get_all_complaints():
        result[complaint["status"]] += 1
    return result