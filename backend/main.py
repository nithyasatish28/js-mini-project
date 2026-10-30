from fastapi import FastAPI, HTTPException 
import functions
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
@app.get("/")
def hello():
    return {"message": "Stations running sucessfully"}

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:5174", "http://127.0.0.1:5174"],
    allow_methods = ["*"],
    allow_headers = ["*"],
)

# @app.post("/stations")
# def create_stations(station_id, name, location, capacity, umbrellas_available):
#     return functions.add_stations(station_id = station_id, name = name, location = location, capacity = 20,umbrellas_available = umbrellas_available)


@app.get("/stations")
def get_stations():
    return functions.get_all_stations()

@app.get("/stations/{station_id}")
def get_stationsbyid(station_id):
    return functions.get_station_by_id(station_id = station_id)

@app.patch("/stations")
def create_stations(station_id, name, location, capacity, umbrellas_available):
    return functions.update_stations(station_id = station_id, name = name, location = location, capacity = 20,umbrellas_available = umbrellas_available)


