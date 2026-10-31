from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import E1

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4001", "http://127.0.0.1:4001"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def hello():
    return {"message": "hello peoples"}


# E1 - Get all plants.
@app.get("/plants")
def read_plants(type: str = None):
    return E1.get_all_plants(type)

# get plant by id
@app.get("/plants/{id}")
def plant(id: int):
    return E1.get_plant(id)


# E3 - new plant inserted
@app.post("/plants", status_code=201)
def create_plant(name: str, type: str, location: str, water_every_days: int):
    return E1.add_plant(name, type, location, water_every_days)

# adopt a plant
@app.patch("/plants/{id}/{roll_no}")
def adopt(id: int, roll_no: str):
    return E1.adopt_plant(id, roll_no.strip())

# watered plant.
@app.post("/plants/{id}/water")
def water_plant(id: int, roll_no: str):
    return E1.water_plant(id, roll_no.strip())

# delete or remove a plant
@app.delete("/plants/{id}", status_code=200)
def delete_plant(id: int):
    return E1.delete_plant(id)

# plants who needs water
@app.get("/plants/needs-water")
def need_water():
    return E1.get_need_water()