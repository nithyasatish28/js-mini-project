import Toshimah_functions
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import AM_functions 

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174","http://127.0.0.1:5174"],
    allow_methods=["*"],
    allow_headers=["*"],
)

Toshimah_functions.seed_data()

 # E1 get all plants info
@app.get("/plants")
def plants(type: str = None):
    return AM_functions.get_all_plants(type)

# E7  get all plants that need  water
@app.get("/plants/needs-water")
def need_water():
    return AM_functions.get_need_water()


# E2
@app.get("/plants/{id}")
def plant(id: int):
    return AM_functions.get_plant(id)



@app.post("/plants")
def add_plant(name, type,location,  water_every_days):
    return Toshimah_functions.add_plant(
        name=name, type=type,  location=location, water_every_days=water_every_days )


# E4
@app.patch("/plants/{id}/{roll_no}")
def adopt(id: int, roll_no: str):
    return AM_functions.adopt_plant(id, roll_no.strip().upper())

@app.patch("/plants/{id}")
def unadopt(id):
    return Toshimah_functions.unadopt_plant(id)


@app.post("/plants/{id}")
def water(plant_id, roll_no):
    return Toshimah_functions.water_plant(plant_id, roll_no)






