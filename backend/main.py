from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import functions

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/complaints")
def show_complaints():
    return functions.get_all_complaints()

@app.get("/complaints/counts")
def complaint_counts():
    return functions.get_complaint_counts()


@app.get("/complaints/{complaint_id}")
def show_complaint(complaint_id: int):
    complaint = functions.get_complaint(complaint_id)
    if complaint is None:
        raise HTTPException(status_code=404, detail="Complaint not found")
    return complaint

@app.post("/complaints", status_code=201)
def add_complaint(roll_no: int, room_no: int, category: str, description: str):
    result = functions.add_complaint(roll_no, room_no, category, description)
    if result is None:
        raise HTTPException(status_code=422, detail="Invalid roll number or room number")
    if result is False:
        raise HTTPException(status_code=409, detail="Duplicate complaint")
    return result
   

@app.patch("/complaints/{complaint_id}/status")
def update_complaint(complaint_id: int, status: str, note: str):
    result = functions.update_complaint(
        complaint_id=complaint_id,
        status=status, note=note
    )
    if result is None:
        raise HTTPException(status_code=404, detail="Complaint not found")
    if result is False:
        raise HTTPException(status_code=409, detail="Invalid status change")
    return result

@app.get("/students/{roll_no}/complaints")
def student_complaints(roll_no: int):

    if roll_no <= 0:
        raise HTTPException(status_code=422, detail="Invalid roll number")
    return functions.get_student_complaints(roll_no)


@app.delete("/complaints/{complaint_id}")
def delete_complaint(complaint_id: int):
    result = functions.delete_complaint(complaint_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Complaint not found")
    if result is False:
        raise HTTPException(status_code=409, detail="Only open complaints can be deleted")
    return {"message": "Complaint deleted successfully"}



