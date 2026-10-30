from fastapi import FastAPI,HTTPException
from fastapi.middleware.cors import CORSMiddleware

import AM_functions

app =FastAPI()

@app.get("/")
def hello():
    return {"Message": "Amruta"}

@app.get("/plants")
def get_plants(type: str = None):
    return AM_functions.get_all_plants(type=type)

@app.get("/plants/{id}")
def get_plant(id: int):
    plant = AM_functions.get_plant(id=id)
    if plant is None:
        raise HTTPException(status_code=404, detail="Plant not found")
    return plant
