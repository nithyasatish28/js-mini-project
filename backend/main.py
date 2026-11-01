from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import functions

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/stations")
def get_all_stations():
    response = functions.get_all_stations()
    return response

@app.get("/stations/needs-attention")
def get_stations_needs_attention():

    response = functions.get_stations_needs_attention()

    return response



@app.get("/stations/{station_id}")
def get_station_by_id(station_id: int):
    response = functions.get_station_by_id(station_id)

    if response is None:
        raise HTTPException(status_code=404, detail="Station not found")

    return response

@app.post("/stations")
def add_station(name: str, location: str, capacity: int, umbrellas_available: int):

    if name.strip() == "" or location.strip() == "":
        raise HTTPException(status_code=422, detail="Name and location cannot be empty")

    if capacity < 1 or capacity > 30:
        raise HTTPException(status_code=422, detail="Capacity must be between 1 and 30")

    if umbrellas_available < 0 or umbrellas_available > capacity:
        raise HTTPException(status_code=422, detail="AvailabilityToBorrow must be between 0 and capacity")

    response = functions.add_station(name, location, capacity, umbrellas_available)

    return response

@app.post("/borrow")
def borrow(roll_no: str, station_id: int):

    if roll_no.strip() == "":
        raise HTTPException(status_code=422, detail="Roll number cannot be empty")

    response = functions.borrow_umbrella(roll_no, station_id)

    if response is None:
        raise HTTPException(status_code=404, detail="Station not found")

    if response == "already_borrowed":
        raise HTTPException(status_code=409, detail="Student already has an unreturned umbrella")

    if response == "no_umbrellas":
        raise HTTPException(status_code=409, detail="No umbrellas available at this station")

    return response

@app.patch("/borrows/{borrow_id}/return")
def return_umbrella(borrow_id: int, station_id: int):

    response = functions.return_umbrella(borrow_id, station_id)

    if response == "borrow_not_found":
        raise HTTPException(status_code=404, detail="Borrow record not found")

    if response == "already_returned":
        raise HTTPException(status_code=409, detail="Umbrella already returned")

    if response == "station_not_found":
        raise HTTPException(status_code=404, detail="Station not found")

    if response == "station_full":
        raise HTTPException(status_code=409, detail="Station is full")

    return response

@app.get("/students/{roll_no}/umbrella")
def get_student_umbrella(roll_no: str):

    response = functions.get_student_umbrella(roll_no)

    if response is None:
        raise HTTPException(status_code=404, detail="Student has no unreturned umbrella")

    return response


