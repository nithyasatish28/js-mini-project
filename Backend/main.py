from fastapi import FastAPI, HTTPException

from Backend import E1
from Backend import E2
from Backend import E3
from Backend import E4
from Backend import E5
from Backend import E6
from Backend import E7


app=FastAPI()

# E1 - Get all equipment
@app.get("/equipment")
def get_equipment():
    return E1.get_all_equipment()

# E1 - Get equipment by type
@app.get("/equipment/type/{equipment_type}")
def get_equipment_by_type(equipment_type: str):
    return E1.get_equipment_by_type(equipment_type)

# E2 - Get equipment by ID
@app.get("/equipment/{equipment_id}")
def get_equipment_by_id(equipment_id: int):
    equipment = E2.get_equipment_by_id(equipment_id)

    if equipment is None:
        raise HTTPException(status_code=404, detail="Equipment not found")

    return equipment

 # E3 - Add new equipment
 
@app.post("/equipment")
def add_equipment(name: str, equipment_type: str, lab_room: str):

    if name.strip() == "":
        raise HTTPException(status_code=422, detail="Equipment name is required")

    if lab_room.strip() == "":
        raise HTTPException(status_code=422, detail="Lab room is required")

    allowed_types = ["microscope", "oscilloscope", "3d-printer", "laptop", "camera"]

    if equipment_type not in allowed_types:
        raise HTTPException(status_code=422, detail="Invalid equipment type")

    return E3.add_equipment(
        name=name,
        type=equipment_type,
        lab_room=lab_room
    )



    
# E4 - Mark equipment status
@app.put("/equipment/{equipment_id}/status")
def mark_equipment_status(equipment_id: int, in_service: bool):
    E4.mark_equipment_status(equipment_id, in_service)
    return {"message": "Equipment status updated successfully."}

# E5 - Book equipment
@app.post("/booking")
def book_equipment(equipment_id: int, roll_no: str, booking_date: str):
    
    if not E5.book_equipment(equipment_id, roll_no, booking_date):
        raise HTTPException(status_code=400, detail="Failed to book equipment")

    return {"message": "Equipment booked successfully."}



# E6 - Get student bookings using roll number
@app.get("/bookings/student/{roll_no}")
def get_student_bookings(roll_no: str):
    return E6.get_student_bookings(roll_no)


# E7 - Cancel booking
@app.patch("/booking/{booking_id}/cancel")
def cancel_booking(booking_id: int):

    result = E7.cancel_booking(booking_id)

    if result is None:
        raise HTTPException(status_code=404, detail="Booking not found")

    if result is False:
        raise HTTPException(status_code=409, detail="Booking already cancelled")

    return {"message": "Booking cancelled successfully."}



