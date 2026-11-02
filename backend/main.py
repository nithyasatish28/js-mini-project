from typing import Optional

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, ConfigDict, Field, field_validator

import functions

app = FastAPI(title="Hostel Complaint Tracker API")


class ComplaintCreate(BaseModel):
    roll_no: int = Field(ge=1)
    room_no: str = Field(min_length=1, max_length=30)
    catagory: Optional[str] = Field(default=None, max_length=80)
    description: str = Field(default="", max_length=1000)
    status: str = Field(default="active", max_length=30)

    @field_validator("room_no", "description", "status")
    @classmethod
    def strip_text(cls, value):
        return value.strip()

    @field_validator("room_no")
    @classmethod
    def require_room_number(cls, value):
        if not value:
            raise ValueError("Room number must not be blank")
        return value

    @field_validator("catagory")
    @classmethod
    def strip_catagory(cls, value):
        if value is None:
            return None
        return value.strip() or None

    @field_validator("status")
    @classmethod
    def normalize_status(cls, value):
        return value.lower()


class ComplaintUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    roll_no: Optional[int] = Field(default=None, ge=1)
    room_no: Optional[str] = Field(default=None, min_length=1, max_length=30)
    catagory: Optional[str] = Field(default=None, max_length=80)
    description: Optional[str] = Field(default=None, max_length=1000)
    status: Optional[str] = Field(default=None, min_length=1, max_length=30)

    @field_validator("roll_no")
    @classmethod
    def reject_null_roll_number(cls, value):
        if value is None:
            raise ValueError("Roll number must not be null")
        return value

    @field_validator("room_no", "status")
    @classmethod
    def strip_required_text(cls, value):
        if value is None:
            raise ValueError("Field must not be null")
        value = value.strip()
        if not value:
            raise ValueError("Field must not be blank")
        return value

    @field_validator("status")
    @classmethod
    def normalize_status(cls, value):
        if value is None:
            raise ValueError("Status must not be null")
        return value.lower()

    @field_validator("catagory", "description")
    @classmethod
    def strip_optional_text(cls, value):
        return value.strip() if value is not None else value


@app.get("/complaints")
def get_all_complaints():
    return functions.get_all_complaints()


@app.get("/complaints/status/{complaint_status}")
def get_complaints_by_status(complaint_status: str):
    normalized_status = complaint_status.strip().lower()
    if normalized_status not in {"active", "pending", "resolved", "closed"}:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Status must be active, pending, resolved, or closed",
        )
    return functions.get_complaints_by_status(normalized_status)


@app.get("/complaints/{complaint_id}")
def get_complaint(complaint_id: int):
    complaint = functions.get_complaint(complaint_id)
    if complaint is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Complaint not found",
        )
    return complaint


@app.post("/complaints", status_code=status.HTTP_201_CREATED)
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
    update_data = data.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Provide at least one field to update",
        )

    complaint = functions.update_complaint(complaint_id, **update_data)
    if complaint is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Complaint not found",
        )
    return complaint


@app.delete("/complaints/{complaint_id}")
def delete_complaint(complaint_id: int):
    deleted = functions.delete_complaint(complaint_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Complaint not found",
        )
    return {"message": "Complaint deleted successfully"}


@app.patch("/complaints/{complaint_id}/resolve")
def resolve_complaint(complaint_id: int):
    complaint = functions.resolve_complaint(complaint_id)
    if complaint is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Complaint not found",
        )
    return complaint
