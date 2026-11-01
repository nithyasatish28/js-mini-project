from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import function 

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8001"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def Hello():
    return {"message": "Hi, Welcome to the Plant API!"}


# E1 - Get all plants.
@app.get("/plants")
def get_plant_data(type: str = None):
    return function.get_all_plants(type)

# E2 - Get plant by id
@app.get("/plants/{id}")
def plant(id: int):
    return function.get_plant(id)


# E3 - new plant inserted
@app.post("/plants", status_code=201)
def create_plant(name: str, type: str, location: str, water_every_days: int):
    return function.add_plant(name, type, location, water_every_days)

# E4 - Adopt a plant
@app.patch("/plants/{id}/{roll_no}")
def adopt(id: int, roll_no: str):
    return function.adopt_plant(id, roll_no.strip())

# E5 - Unadopt a plant.
@app.patch("/plants/{id}/unadopt")
def unadopt_plant(id: int):
    return function.unadopt_plant(id)

# E6 - watered plant.
@app.post("/plants/{id}/water")
def water_plant(id: int, roll_no: str):
    return function.water_plant(id, roll_no.strip())


# E7 - plants who needs water
@app.get("/plants/needs-water")
def need_water():
    return function.get_need_water()