from fastapi import FastAPI
import functions

app = FastAPI()

@app.get("/equipments")
def get_all_equipment(type : str = None):
    return functions.get_all_equipment(type)


@app.get("/equipments/{id}")
def get_equipment(id : int):
    return functions.get_equipment(id)

@app.post("/equipments", status_code=201)
def add_equipment(name : str, type : str, lab_room : str):
    return functions.add_equipment(name=name, type=type, lab_room=lab_room)


@app.get("/equipments")
def get_all_equipment(type : str = None):
    return functions.get_all_equipment(type)



@app.get("/equipments/{id}")
def get_equipment(id : int):
    return functions.get_equipment(id)



@app.post("/equipments", status_code=201)
def add_equipment(name : str, type : str, lab_room : str):
    return functions.add_equipment(name=name, type=type, lab_room=lab_room)




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
