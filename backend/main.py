from fastapi import FastAPI, HTTPException
import functions
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/equipments")
def get_all_equipment(type : str = None):
    return functions.get_all_equipment(type)


@app.get("/equipments/{id}")
def get_equipment(id : int):
    return functions.get_equipment(id)

@app.post("/equipments", status_code=201)
def add_equipment(name : str, type : str, lab_room : str):
    return functions.add_equipment(name=name, type=type, lab_room=lab_room)


@app.patch("/equipments/status/{equipment_id}")
def update_service(equipment_id : int, in_service : bool):
    functions.update_service(equipment_id, in_service)
    return {"message": "Equipment status updated successfully."}


@app.post("/booking")
def add_booking(equipment_id : int, booking_date : str, roll_no : str):
    return functions.add_booking(equipment_id=equipment_id, booking_date=booking_date, roll_no=roll_no)

@app.get("/booking/{roll_no}")
def get_equipments_not_booked(roll_no : str):
    return functions.get_student_bookings(roll_no)

@app.patch("/booking/cancel/{id_or_roll}")
def cancel_booking(id_or_roll : str, booking_id : int = None):
    if booking_id is not None:
        target_id = booking_id
    else:
        try:
            target_id = int(id_or_roll)
        except ValueError:
            raise HTTPException(status_code=422, detail="Booking id must be an integer.")
    return functions.cancel_booking(target_id)
