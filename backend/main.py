from fastapi import FastAPI, HTTPException

from backend import functions
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Umbrella Sharing API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"]
)
# E1 - Get all stations
@app.get("/stations")
def get_all_stations():
    return functions.get_all_stations()


# E7 - Get stations needing attention
@app.get("/stations/needs-attention")
def get_stations_needing_attention():
    return functions.get_stations_needing_attention()


# E2 - Get one station
@app.get("/stations/{station_id}")
def get_station(station_id: int):
    station = functions.get_station(station_id)

    if station is None:
        raise HTTPException(status_code=404,detail="Station not found error")

    return station


# E3 - Add a new station
@app.post("/stations", status_code=201)
def add_station(
    name: str,
    location: str,
    capacity: int,
    umbrellas_available: int
):
    result = functions.add_station(name,location,capacity,umbrellas_available)

    if "error" in result:
        raise HTTPException(status_code=result["status_code"],
            detail=result["error"]
        )
    return result


# E4 - Borrow an umbrella
@app.post("/stations/{station_id}/borrow", status_code=201)
def borrow_umbrella(station_id: int, roll_no: str):
    result = functions.borrow_umbrella(station_id, roll_no)

    if "error" in result:
        raise HTTPException(status_code=result["status_code"],
            detail=result["error"]
        )

    return result


# E5 - Return an umbrella
@app.patch("/borrows/{borrow_id}/return")
def return_umbrella(borrow_id: int, to_station_id: int):
    result = functions.return_umbrella(borrow_id,to_station_id)

    if "error" in result:
        raise HTTPException(status_code=result["status_code"],
            detail=result["error"]
        )
    return result


# E6 - Get student's active umbrella
@app.get("/borrows/active/{roll_no}")
def get_active_borrow(roll_no: str):
    result = functions.get_active_borrow(roll_no)

    if result is None:
        raise HTTPException(status_code=404,detail="No active umbrella found"
        )

    return result