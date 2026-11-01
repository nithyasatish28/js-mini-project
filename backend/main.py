from datetime import date, datetime, timedelta
from fastapi import FastAPI, HTTPException, Body, Query
from fastapi.middleware.cors import CORSMiddleware
import function

app = FastAPI(title="Laboratory Equipment Booking System")

app.add_middleware(
    __import__("fastapi").middleware.cors.CORSMiddleware,
    allow_origins=["http://localhost:5173","http://127.0.0.1:5173"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"]
)



@app.get("/equipment")
def equipment(type: str = None):
    if type is not None and type not in function.VALID_TYPES:
        raise HTTPException(status_code=422,detail="Invalid equipment type.")
    return function.get_all_equipment(type=type)


@app.get("/equipment/{id}")
def equipment_by_id(id: int):
    result = function.get_equipment(id)
    if result is None:
        raise HTTPException(status_code=404,detail="Equipment not found.")
    return result


@app.post("/equipment", status_code=201)
def add_equipment(name: str = Body(...),type: str = Body(...),lab_room: str = Body(...)):
    if not name.strip() or not lab_room.strip():
        raise HTTPException(status_code=422,detail="Name and lab room cannot be empty.")
    if type not in function.VALID_TYPES:
        raise HTTPException(status_code=422,detail="Invalid equipment type.")
    return function.add_equipment(name=name,item_type=type,lab_room=lab_room)


@app.patch("/equipment/{id}/service")
def change_service_status(id: int,in_service: int = Body(...)):
    if in_service not in [0, 1]:
        raise HTTPException(status_code=422,detail="Service status must be 0 or 1.")
    result = function.update_service(id=id,in_service=in_service)

    if result is None:
        raise HTTPException(status_code=404,detail="Equipment not found.")
    return result


@app.post("/bookings", status_code=201)
def book_equipment(equipment_id: int = Body(...),roll_no: str = Body(...),booking_date: str = Body(...)):
    if not roll_no.strip():
        raise HTTPException(status_code=422,detail="Roll number cannot be empty.")
    result = function.book_equipment(equipment_id=equipment_id,roll_no=roll_no,booking_date=booking_date)
    if "error" in result:
        raise HTTPException(status_code=result["error"],detail=result["detail"])
    return result


@app.get("/bookings")
def student_bookings(roll_no: str = Query(...)):
    if not roll_no.strip():
        raise HTTPException(status_code=422,detail="Roll number cannot be empty.")
    return function.get_student_bookings(roll_no)


@app.patch("/bookings/{id}/cancel",
    responses={404: {"description": "Booking not found"}, 409: {"description": "Booking is already cancelled"}})
def cancel_booking(id: int):
    result = function.cancel_booking(id)
    if result is None:
        raise HTTPException(status_code=404,detail="Booking not found.")
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=result["error"],detail=result["detail"])

    return result
    
