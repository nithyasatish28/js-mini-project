from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

import function

app = FastAPI()

class StationCreate(BaseModel):
    name: str = Field(min_length=1)
    location: str = Field(min_length=1)
    capacity: int = Field(ge=1, le=30)
    umbrellas_available: int = Field(ge=0)


@app.on_event("startup")
def startup():
    function.add_initial_stations()


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

        raise HTTPException(status_code=422, detail="Umbrellas available cannot exceed capacity")

    return function.add_station(

        name=station.name,
        location=station.location,
        capacity=station.capacity,
        umbrellas_available=station.umbrellas_available

    )