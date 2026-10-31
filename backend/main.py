from fastapi import FastAPI, HTTPException
import function

app = FastAPI()


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