from fastapi import FastAPI , HTTPException
from fastapi.middleware.cors import CORSMiddleware
import functions

app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173","http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"])

@app.get("/plants")
def plants():
    return functions.get_all_plants()


@app.get("/plants/{id}")
def plants_by_id(id: int):
    # return functions.get_all_plants(id=id)
    plant=functions.get_plant_by_id(id=id)
    if plant is None:
        raise HTTPException(status_code=404,detail="plant not found")
    return plant


@app.post("/plants")
def plants_new(name: int,type: str,location: str,water_every_days: str):
    allowed_type = ["succulent","flowering","herb","indoor","tree"]
    if type is not allowed_type:
        raise HTTPException(status_code=422,detail="invalid type ")

    return functions.add_plant(name=name,type=type,location=location,water_every_days=water_every_days)
    

@app.post("/waterings/plants")
def plants_adopt(roll_no: int,plant_id:int):  
    return functions.adopt_plant(roll_no=roll_no,plant_id=plant_id)

@app.patch("/plants/{id}")
def plants_not_adopted(plant_id:int):
    return functions.give_up_plant(plant_id=plant_id)

@app.post("/waterings/{plant_id}")
def plants_log(plant_id:int,roll_no:int,watered_on:int):
    return functions.get_all_Waterings(plant_id=plant_id,roll_no=roll_no,watered_on=watered_on)

@app.get("/plants/want_water")
def plants_today(id:int,water_every_days:int):
    return functions.get_all_plants(id=id,water_every_days=water_every_days)

