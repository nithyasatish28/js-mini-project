from fastapi import FastAPI, status, HTTPException
from fastapi.responses import RedirectResponse
from backend import functions


app = FastAPI(title="Umbrella Sharing API")


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")


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
        raise HTTPException(
            status_code=404,
            detail="Station not found."
        )

    return station


# E3 - Add a new station
@app.post("/stations", status_code=status.HTTP_201_CREATED)
def add_station(station: dict):

    result = functions.add_station(
        station.get("name"),
        station.get("location"),
        station.get("capacity"),
        station.get("umbrellas_available")
    )

    if "error" in result:
        raise HTTPException(
            status_code=result["status_code"],
            detail=result["error"]
        )

    return result


# E4 - Borrow an umbrella
@app.post(
    "/stations/{station_id}/borrow",
    status_code=status.HTTP_201_CREATED
)
def borrow_umbrella(station_id: int, student: dict):

    result = functions.borrow_umbrella(
        station_id,
        student.get("roll_no")
    )

    if "error" in result:
        raise HTTPException(
            status_code=result["status_code"],
            detail=result["error"]
        )

    return result


# E5 - Return an umbrella
@app.patch("/borrows/{borrow_id}/return")
def return_umbrella(borrow_id: int, station: dict):

    to_station_id = station.get("to_station_id")

    if type(to_station_id) is not int or to_station_id <= 0:
        raise HTTPException(
            status_code=422,
            detail="A valid to_station_id is required."
        )

    result = functions.return_umbrella(
        borrow_id,
        to_station_id
    )

    if "error" in result:
        raise HTTPException(
            status_code=result["status_code"],
            detail=result["error"]
        )

    return result


# E6 - Get student's active umbrella
@app.get("/borrows/active/{roll_no}")
def get_active_borrow(roll_no: str):

    result = functions.get_active_borrow(roll_no)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="No active umbrella found for this student."
        )

    return result