from fastapi import FastAPI, HTTPException 
import functions
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
@app.get("/")
def hello():
    return {"message": "Stations running sucessfully"}

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods = ["*"],
    allow_headers = ["*"],
)

@app.post("/stations")
def Add_stations(name, location, capacity: int, umbrellas_available: int):
    if capacity < 1 or capacity > 30:
            raise HTTPException(status_code=422,detail="Capacity must be between 1 and 30.")
    
    if umbrellas_available < 0 or umbrellas_available > capacity:
            raise HTTPException(status_code=422,detail="Starting umbrellas must be between 0 and capacity.")
    
    return functions.add_stations(name = name, location = location, capacity = capacity, umbrellas_available = umbrellas_available)


@app.get("/stations")
def get_stations():
    return functions.get_all_stations()

@app.get("/stations/attention")
def get_attention_stations():

    return functions.get_attention_stations()


@app.get("/stations/{station_id}")
def get_stationsbyid(station_id):

    if functions.get_station_by_id(station_id=station_id) is None:
        raise HTTPException(status_code=404, detail="Station not found."
        )

    return functions.get_station_by_id(station_id=station_id)


@app.post("/borrows")
def borrow_umbrella(roll_no, station_id):

    if not roll_no:
        raise HTTPException(status_code=422,detail="Roll number is required.")

    if not station_id:
        raise HTTPException(status_code=422,detail="Station ID is required.")

    if functions.get_station_by_id(station_id=station_id) is None:
        raise HTTPException(status_code=404,detail="Station not found.")

    Station = functions.get_station_by_id(station_id=station_id)

    if Station["umbrellas_available"] == 0:
        raise HTTPException(status_code=409,detail="This station is empty.")

    if functions.get_active_borrow(roll_no=roll_no) is not None:
        raise HTTPException(status_code=409,detail="You already have an umbrella. Return it first.")

    return functions.borrow_umbrella(
        roll_no=roll_no,
        station_id=station_id
    )


@app.patch("/borrows/{roll_no}/return")
def return_umbrella(roll_no, station_id):

    if not roll_no: 
        raise HTTPException(status_code=422,detail="Roll number is required.")

    if not station_id: 
        raise HTTPException(status_code=422,detail="Station ID is required.")

    Station = functions.get_station_by_id(station_id=station_id)

    if Station is None:
        raise HTTPException(status_code=404,detail="Station not found.")

    if Station["capacity"] == Station["umbrellas_available"]:
        raise HTTPException(status_code=409,detail="This station is full. Try another one.")

    if functions.get_active_borrow(roll_no=roll_no) is None:
        raise HTTPException(status_code=409,detail="You don't have an active umbrella to return.")

    return functions.return_umbrella(roll_no=roll_no,station_id=station_id)


@app.get("/borrows/active")
def get_student_borrow(roll_no):

    if not roll_no:
        raise HTTPException(status_code=422,detail="Roll number is required.")

    if functions.get_student_borrow(roll_no=roll_no) is None:
        raise HTTPException(status_code=404,detail="No active umbrella found for this student.")

    return functions.get_student_borrow(roll_no=roll_no)


# @app.get("/stations/attention")
# def get_attention_stations():

#     return functions.get_attention_stations()
