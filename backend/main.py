from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
<<<<<<< Updated upstream
import E1
import E2
import E3
import E4
import E5
import E6
import E7
=======
import function
>>>>>>> Stashed changes

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
<<<<<<< Updated upstream
def get_plant_data(type: str = None):
    return E1.get_all_plants(type)
=======
def read_plants(type: str = None):
    return function.get_all_plants(type)
>>>>>>> Stashed changes

# E2 - Get plant by id
@app.get("/plants/{id}")
<<<<<<< Updated upstream
def read_plant(id: int):
    return E2.get_plant(id)
=======
def plant(id: int):
    return function.get_plant(id)
>>>>>>> Stashed changes


# E3 - new plant inserted
@app.post("/plants", status_code=201)
def create_plant(name: str, type: str, location: str, water_every_days: int):
<<<<<<< Updated upstream
    return E3.add_plant(name, type, location, water_every_days)
=======
    return function.add_plant(name, type, location, water_every_days)
>>>>>>> Stashed changes

# E4 - Adopt a plant
@app.patch("/plants/{id}/{roll_no}")
def adopt(id: int, roll_no: str):
<<<<<<< Updated upstream
    return E4.adopt_plant(id, roll_no.strip())
=======
    return function.adopt_plant(id, roll_no.strip())
>>>>>>> Stashed changes

# watered plant.
@app.post("/plants/{id}/water")
def water_plant(id: int, roll_no: str):
<<<<<<< Updated upstream
    return E5.water_plant(id, roll_no.strip())
=======
    return function.water_plant(id, roll_no.strip())
>>>>>>> Stashed changes

# delete or remove a plant
@app.delete("/plants/{id}", status_code=200)
def delete_plant(id: int):
    return function.delete_plant(id)

# plants who needs water
@app.get("/plants/needs-water")
def need_water():
<<<<<<< Updated upstream
    return E7.get_need_water()
=======
    return function.get_need_water()
>>>>>>> Stashed changes
