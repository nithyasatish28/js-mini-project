from datetime import datetime

from fastapi import FastAPI
import functions

app = FastAPI()


@app.patch("/equipments{equipment_id}/status")
def update_service(equipment_id : int, in_service : bool):
    functions.update_service(equipment_id,in_service)
    return {"message": "Equipment status updated successfully."}


@app.post("/booking")
def add_booking(equipment_id : int ,booking_date , roll_no : int):
    return functions.add_booking(equipment_id=equipment_id, booking_date=booking_date, roll_no=roll_no)

@app.get("/booking/{roll_no}")
def get_equipments_not_booked(roll_no):
    return functions.get_student_bookings(roll_no)

@app.patch("/booking/cancel/{roll_no}")
def cancel_booking(booking_id : int):
    return functions.cancel_booking(booking_id)
