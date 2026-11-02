from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import functions


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173","http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.post("/students", status_code=201)
def student(roll_no, name, contact):

    result = functions.add_student(roll_no=roll_no,name=name,contact=contact)

    if result.get("message") == "Student already exists":
        raise HTTPException(status_code=409, detail="Student already exists")

    return result

@app.get("/stations")
def stations():
    return functions.get_all_stations()

@app.get("/stations/attention")
def attention_stations():
    return functions.get_attention_stations()

@app.get("/stations/{id}")
def station(id: int):

    result = functions.get_station(id)

    if result is None:
        raise HTTPException(status_code=404, detail="Station not found")

    return result

@app.post("/stations", status_code=201)
def add_station(name, location, capacity: int, umbrellas_available: int):

    if capacity < 1 or capacity > 30:
        raise HTTPException(status_code=422, detail="Capacity must be between 1 and 30")

    if umbrellas_available < 0 or umbrellas_available > capacity:
        raise HTTPException(status_code=422, detail="Invalid umbrella count")

    return functions.add_station(name=name,location=location,capacity=capacity,umbrellas_available=umbrellas_available)

@app.post("/borrow")
def borrow(roll_no, station_id: int):

    result = functions.borrow_umbrella(roll_no=roll_no,station_id=station_id)

    errors = {
        "Student not found": 404,
        "Station not found": 404,
        "No umbrellas available": 409,
        "Already borrowed": 409
    }

    if result.get("message") in errors:
        raise HTTPException(status_code=errors[result["message"]],detail=result["message"])

    return result


@app.post("/return")
def return_umbrella(roll_no, station_id: int):

    result = functions.return_umbrella(roll_no=roll_no,station_id=station_id)

    errors = {
        "Student not found": 404,
        "No umbrella borrowed": 409,
        "Station not found": 404,
        "Station is full": 409
    }

    if result.get("message") in errors:
        raise HTTPException(
            status_code=errors[result["message"]],
            detail=result["message"]
        )

    return result

@app.get("/student/{roll_no}/borrow")
def student_borrow(roll_no):

    result = functions.get_student_borrow(roll_no)

    if result.get("message") == "Student not found":
        raise HTTPException(status_code=404, detail="Student not found")

    if result.get("message") == "No unreturned umbrella found":
        raise HTTPException(status_code=404, detail="No unreturned umbrella found")

    return result