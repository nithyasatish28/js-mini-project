from fastapi import FastAPI,HTTPException
from fastapi.middleware.cors import CORSMiddleware

import AM_functions 

from typing import Literal

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

@app.get("/")
def hello():
    return {"Message": "Amruta"}


import Toshimah_functions

Toshimah_functions.seed_data()


PlantType = Literal["succulent", "flowering", "herb", "indoor", "tree"]


# E1 get all plants info
@app.get("/plants")
def plants(type: PlantType = None):
    return AM_functions.get_all_plants(type)

# E7  get all plants that need  water
@app.get("/plants/needs-water")
def need_water():
    return AM_functions.get_need_water()

# E2
@app.get("/plants/{id}")
def plant(id: int):
    return AM_functions.get_plant(id)


# E4
@app.patch("/plants/{id}/{roll_no}")
def adopt(id: int, roll_no: str):
    return AM_functions.adopt_plant(id, roll_no.strip())




