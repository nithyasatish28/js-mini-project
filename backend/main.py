from typing import Optional

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

import functions

app = FastAPI(title="Complaints API")


class ComplaintCreate(BaseModel):
    roll_no: int
    room_no: str
    catagory: Optional[str] = None
    description: str = ""
    status: str = "active"


class ComplaintUpdate(BaseModel):
    roll_no: Optional[int] = None
    room_no: Optional[str] = None
    catagory: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    resolved_on: Optional[str] = None


@app.get("/complaints")
def get_all_complaints():
    return functions.get_all_Complaints()


@app.get("/complaints/{complaint_id}")
def get_complaint(complaint_id: int):
    complaint = functions.get_Complaints(complaint_id)
    if complaint is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Complaint not found")
    return complaint


@app.post("/complaints")
def create_complaint(data: ComplaintCreate):
    return functions.add_complaint(
        roll_no=data.roll_no,
        room_no=data.room_no,
        catagory=data.catagory,
        description=data.description,
        status=data.status,
    )

@app.put("/complaints/{complaint_id}")
def update_complaint(complaint_id: int, data: ComplaintUpdate):
    update_data = {k: v for k, v in data.dict(exclude_unset=True).items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Fill all the fields")

    complaint = functions.update_complaint(complaint_id)
    if complaint is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Complaint NAHI MAL. COMPLAINT DAAL!!!!")
    return complaint


@app.delete("/complaints/{complaint_id}")
def delete_complaint(complaint_id: int):
    deleted = functions.delete_complaint(complaint_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Complaint not found")
    return {"message": "Complaint deleted successfully"}

