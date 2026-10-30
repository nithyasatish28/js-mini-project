from fastapi import FastAPI, HTTPException
from datetime import date
import functions

app = FastAPI()


@app.get("/equipment")
def get_equipment():
    return functions.get_all_equipments() 

@app.get("/equipment/type/{equipment_type}")
def get_equipment_by_type(equipment_type: str):
    return functions.get_equipment_by_type(equipment_type)

@app.get("/equipment/{equipment_id}")
def equipment_by_id(equipment_id: int):

    if functions.get_equipment_by_id(equipment_id=equipment_id) is None:
        raise HTTPException(status_code=404, detail="Equipment not found")

    return functions.get_equipment_by_id(equipment_id=equipment_id)


@app.post("/equipment")
def add_equipment(name, equipment_type, lab_room):

    if not name or not lab_room or not equipment_type:
        raise HTTPException(status_code=422, detail="All fields are required")

    if equipment_type not in functions.equipment_types:
        raise HTTPException(status_code=422, detail="Invalid equipment type")

    return functions.add_equipment(name=name,equipment_type=equipment_type,lab_room=lab_room)

@app.patch("/equipment/{equipment_id}")
def update_service(equipment_id: int, in_service: int):

    if in_service not in [0, 1]:
        raise HTTPException(status_code=422, detail="Invalid service status")

    result = functions.update_service(equipment_id, in_service)

    if result is None:
        raise HTTPException(status_code=404, detail="Equipment not found")

    return result


from datetime import date

@app.post("/bookings", status_code=201)
def book_equipment(equipment_id: int, roll_no: str, booking_date: date):

    if not roll_no.strip():
        raise HTTPException(status_code=422, detail="Roll number is required")

    if booking_date < date.today():
        raise HTTPException(status_code=422, detail="Past date not allowed")

    if (booking_date - date.today()).days > 7:
        raise HTTPException(status_code=422, detail="Booking date cannot be more than 7 days ahead")

    result = functions.book_equipment(equipment_id, roll_no, booking_date)

    if result is None:
        raise HTTPException(status_code=404, detail="Equipment not found")

    if result == "out_of_service":
        raise HTTPException(status_code=409, detail="Equipment is out of service")

    if result == "already_booked":
        raise HTTPException(status_code=409, detail="Equipment is already booked for this date")

    if result == "booking_limit":
        raise HTTPException(status_code=409, detail="Maximum 2 bookings allowed per day")

    return result  


@app.get("/students/{roll_no}/bookings")
def student_bookings(roll_no):
    if not roll_no:
        raise HTTPException(status_code=422, detail="Roll number is required")

    return functions.get_student_bookings(roll_no=roll_no)  

@app.patch("/bookings/{booking_id}/cancel")
def cancel_booking(booking_id):
    booking = functions.get_booking(booking_id)

    if booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")

    if booking.cancelled == 1:
        raise HTTPException(status_code=409, detail="Booking is already cancelled")

    return functions.cancel_booking(booking_id)