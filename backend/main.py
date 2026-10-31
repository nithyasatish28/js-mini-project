from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import function

app = FastAPI()


@app.on_event("startup")
def startup():
    function.add_initial_stations()


class StationCreate(BaseModel):
    name: str = Field(min_length=1)
    location: str = Field(min_length=1)
    capacity: int = Field(ge=1, le=30)
    umbrellas_available: int = Field(ge=0)


class BorrowCreate(BaseModel):
    roll_no: str = Field(pattern=r"^R[1-9][0-9]*$")
    from_station_id: int = Field(ge=1)


class ReturnCreate(BaseModel):
    to_station_id: int = Field(ge=1)


@app.get("/")
def hello():
    return {"message": "Umbrella Sharing API is running"}


@app.get("/stations")
def get_all_stations():
    return function.get_all_stations()


@app.get("/stations/{station_id}")
def get_station(station_id: int):
    station = function.get_station(station_id)

    if station is None:
        raise HTTPException(status_code=404, detail="Station not found")

    return station


@app.post("/stations")
def add_station(station: StationCreate):
    if station.umbrellas_available > station.capacity:
        raise HTTPException(
            status_code=400,
            detail="Umbrellas available cannot exceed capacity"
        )

    return function.add_station(
        name=station.name,
        location=station.location,
        capacity=station.capacity,
        umbrellas_available=station.umbrellas_available
    )


@app.post("/borrow")
def borrow_umbrella(borrow: BorrowCreate):
    result = function.borrow_umbrella(
        roll_no=borrow.roll_no,
        from_station_id=borrow.from_station_id
    )

    if "error" in result:
        raise HTTPException(
            status_code=result["status_code"],
            detail=result["error"]
        )

    return result


@app.patch("/return/{borrow_id}")
def return_umbrella(borrow_id: int, return_data: ReturnCreate):
    result = function.return_umbrella(
        borrow_id=borrow_id,
        to_station_id=return_data.to_station_id
    )

    if "error" in result:
        raise HTTPException(
            status_code=result["status_code"],
            detail=result["error"]
        )

    return result