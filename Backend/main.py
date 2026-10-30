from fastapi import FastAPI, HTTPException
<<<<<<< Updated upstream
from Backend import E1
from Backend import E2
from Backend import E4
from Backend import E5


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
=======
from Backend import E1, E2, E3, E6

app = FastAPI()


# E6 - Get student bookings using roll number
@app.get("/bookings/student/{roll_no}")
def get_student_bookings(roll_no: str):
    return E6.get_student_bookings(roll_no)
>>>>>>> Stashed changes
