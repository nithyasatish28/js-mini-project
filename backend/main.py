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
def get_equipment_by_id(equipment_id: int):
    equipment = functions.get_equipment_by_id(equipment_id)

    if equipment is None:
        raise HTTPException(status_code=404, detail="Equipment not found")

    return equipment


@app.post("/equipment")
def add_equipment(name: str, equipment_type: str, lab_room: str):
    if not name or not equipment_type or not lab_room:
        raise HTTPException(status_code=422, detail="All fields are required")

    if equipment_type not in functions.equipment_types:
        raise HTTPException(status_code=422, detail="Invalid equipment type")

    return functions.add_equipment(
        name=name,
        equipment_type=equipment_type,
        lab_room=lab_room
    )


@app.patch("/equipment/{equipment_id}")
def update_service(equipment_id: int, in_service: int):
    if in_service not in [0, 1]:
        raise HTTPException(status_code=422, detail="Invalid service status")

    response = functions.update_service(equipment_id, in_service)

    if response is None:
        raise HTTPException(status_code=404, detail="Equipment not found")

    return response


@app.post("/bookings")
def book_equipment(equipment_id: int, roll_no: str, booking_date: date):
    if not roll_no.strip():
        raise HTTPException(status_code=422, detail="Roll number is required")

    if booking_date < date.today():
        raise HTTPException(status_code=422, detail="Past date not allowed")

    if (booking_date - date.today()).days > 7:
        raise HTTPException(
            status_code=422,
            detail="Booking date cannot be more than 7 days ahead"
        )

    response = functions.book_equipment(
        equipment_id,
        roll_no,
        booking_date
    )

    if response is None:
        raise HTTPException(status_code=404, detail="Equipment not found")

    if response == "out_of_service":
        raise HTTPException(status_code=409, detail="Equipment is out of service")

    if response == "already_booked":
        raise HTTPException(
            status_code=409,
            detail="Equipment is already booked for this date"
        )

    if response == "booking_limit":
        raise HTTPException(
            status_code=409,
            detail="Maximum 2 bookings allowed per day"
        )

    return response


@app.get("/students/{roll_no}/bookings")
def student_bookings(roll_no: str):
    if not roll_no:
        raise HTTPException(status_code=422, detail="Roll number is required")

    return functions.get_student_bookings(roll_no)


@app.patch("/bookings/{booking_id}/cancel")
def cancel_booking(booking_id: int):
    booking = functions.get_booking(booking_id)

    if booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")

    if booking.cancelled == 1:
        raise HTTPException(status_code=409, detail="Booking is already cancelled")

    return functions.cancel_booking(booking_id)
