

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import functions
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
def hello():
    return {"message": "Garden API is running"}


# E1 - Get all plants

@app.get("/plants")
def plants():
    return functions.get_all_plants()

# E7 - Get plants needing water

@app.get("/plants/needs-water")
def needs_water():
    return functions.plants_need_water()


# E2 - Get one plant with watering history
@app.get("/plants/{plant_id}")
def plant(plant_id: int):

    result = functions.get_plant_by_id(plant_id)
    if result is None:raise HTTPException(status_code=404,detail="Plant not found")
    return result


# E3 - Add a new plant
@app.post("/plants")
def add_plant(name: str,type: str,water_every_days: int,location: str = None):
    allowed_types = ["succulent","flowering","herb","indoor","tree" ]
    if type not in allowed_types:
        raise HTTPException(status_code=422,detail="Invalid plant type")
    if water_every_days < 1 or water_every_days > 14:
        raise HTTPException(status_code=422,detail="Watering days must be between 1 and 14")

    return functions.add_plant(name=name,type=type,location=location,water_every_days=water_every_days)

# E4 - Adopt a plant

@app.post("/plants/{plant_id}/adopt")
def adopt_plant(plant_id: int, roll_no: str):
    return functions.adopt_plant(plant_id=plant_id,roll_no=roll_no)

# E5 - Give up a plant

@app.delete("/plants/{plant_id}/adopt")
def give_up_plant(plant_id: int):
    return functions.give_up_plant(plant_id=plant_id)



# E6 - Water a plant

@app.post("/plants/{plant_id}/water")
def water_plant(plant_id: int, roll_no: str,watered_on:str):
    watered_on = datetime.strptime(watered_on, "%d/%m/%Y").date()
    if watered_on > datetime.now().date():
        raise HTTPException(status_code=422,detail="Watering date cannot be in the future")
    return functions.add_waterings(plant_id=plant_id,roll_no=roll_no,watered_on=watered_on)

