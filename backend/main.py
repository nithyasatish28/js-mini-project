<<<<<<< HEAD
from fastapi import FastAPI,HTTPException
from fastapi.middleware.cors import CORSMiddleware

import AM_functions
=======
from typing import Literal
from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
import function
>>>>>>> df399db81b6cb33d4823d8cfe08fe7a2f57ba2c9

app = FastAPI()

<<<<<<< HEAD
@app.get("/")
def hello():
    return {"Message": "Amruta"}

@app.get("/plants")
def get_plants(type: str = None):
    return AM_functions.get_all_plants(type=type)
=======
# lets the React app (port 5173) call this API (port 8001)
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173"],
                   allow_methods=["*"], allow_headers=["*"])

function.seed()

PlantType = Literal["succulent", "flowering", "herb", "indoor", "tree"]


# E1
@app.get("/plants")
def plants(type: PlantType = None):
    return function.get_all_plants(type)
>>>>>>> df399db81b6cb33d4823d8cfe08fe7a2f57ba2c9

# E7  (must be above /plants/{id})
@app.get("/plants/needs-water")
def needs_water():
    return function.get_needs_water()

# E2
@app.get("/plants/{id}")
def plant(id: int):
    return function.get_plant(id)

# E3
@app.post("/plants", status_code=201)
def add_plant(name: str = Body(pattern=r"\S"), type: PlantType = Body(),
              location: str = Body(pattern=r"\S"), water_every_days: int = Body(ge=1, le=14)):
    return function.add_plant(name=name.strip(), type=type, location=location.strip(),
                              water_every_days=water_every_days)

# E4
@app.patch("/plants/{id}/adopt")
def adopt(id: int, roll_no: str = Body(embed=True, pattern=r"\S")):
    return function.adopt_plant(id, roll_no.strip())

# E5
@app.patch("/plants/{id}/unadopt")
def unadopt(id: int):
    return function.unadopt_plant(id)

# E6
@app.post("/plants/{id}/waterings", status_code=201)
def water(id: int, roll_no: str = Body(embed=True, pattern=r"\S")):
    return function.water_plant(id, roll_no.strip())
