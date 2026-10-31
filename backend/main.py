import Toshimah_functions
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174   "],
    allow_methods=["*"],
    allow_headers=["*"],
)

Toshimah_functions.seed_data()



@app.post("/plants")
def add_plant(name, type,location,  water_every_days):
    return Toshimah_functions.add_plant(
        name=name, type=type,  location=location, water_every_days=water_every_days )


@app.patch("/plants/{id}")
def unadopt(id):
    return Toshimah_functions.unadopt_plant(id)


@app.post("/plants/{id}")
def water(plant_id, roll_no):
    return Toshimah_functions.water_plant(plant_id, roll_no)

 