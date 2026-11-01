from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import function 

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174","http://127.0.0.1:5174" ],
    allow_methods=["*"],
    allow_headers=["*"]
)

class PlantCreate(BaseModel):
 name: str
 type: str
 location: str
 water_every_days: int
class AdoptRequest(BaseModel):
 roll_no: str
class WaterRequest(BaseModel):
 roll_no: str


@app.get("/")
def Hello():
    return {"message": "Hi, Welcome to the Plant API!"}


# E1 - Get all plants.
@app.get("/plants")
def get_plant_data(type: str = None):
    return function.get_all_plants(type)


# E7 - plants who needs water
@app.get("/plants/need-water")
def need_water():
    return function.get_need_water()

# E2 - Get plant by id
@app.get("/plants/{id}")
def get_single_plant(id: int): 
    return function.get_plant(id)


# E3 - new plant inserted
@app.post("/plants", status_code=201)
def create_plant(plant: PlantCreate):
    return function.add_plant(plant.name, plant.type, plant.location, plant.water_every_days)

# E5 - Unadopt a plant.
@app.patch("/plants/{id}/unadopt")
def unadopt_plant(id: int):
    return function.unadopt_plant(id)


# E4 - Adopt a plant    
@app.patch("/plants/{id}/adopt")
def adopt(id: int, request: AdoptRequest):
    return function.adopt_plant(id, request.roll_no.strip())

@app.patch("/plants/{id}/{roll_no}")
def adopt_plant_path(id: int, roll_no: str):
 return function.adopt_plant(id, roll_no.strip())


# E6 - watered plant.
@app.post("/plants/{id}/water")
def water_plant(id: int, req: WaterRequest = None, roll_no: str = None):
 actual_roll = req.roll_no if req else roll_no
 if not actual_roll:
    raise HTTPException(status_code=422, detail="roll_no is required")
 return function.water_plant(id, actual_roll.strip())