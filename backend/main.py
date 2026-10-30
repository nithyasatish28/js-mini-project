from urllib import response

from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
import functions


app = FastAPI()

app.add_middleware(CORSMiddleware,
                   allow_origins=["http://localhost:5173"],
                   allow_methods=["*"],
                   allow_headers=["*"])

# this is used both for adopting and giving up where {adopted_by: null} means its giving up
@app.patch("/plants/{plant_id}")
def adopt_plant(plant_id: str, body=Body()):
    adopted_by = body["adopted_by"]
    if adopted_by:
        response = functions.adopt_plant(plant_id=plant_id,roll_no=adopted_by)
        code = response["code"]
        if code == 200:
            return response["plant"]
        raise HTTPException(code,detail=response["msg"])

    response = functions.give_up_plant(plant_id=plant_id)
    code = response["code"]
    if code == 200:
        return response["plant"]
    raise HTTPException(code, detail=response["msg"])

@app.post("/water")
def water(body = Body()):
    response = functions.water_plant( body["plant_id"], body["roll_no"])
    code = response["code"]
    if code == 200:
        return response["watering"]
    raise HTTPException(code, detail=response["msg"])



@app.get("/plants")
def plants(plant_type=None):
    return functions.get_all_plants(plant_type=plant_type)


@app.post("/plants")
def add_plant(name,type,location,water_every_days):
    return  functions.add_plant(name=name,type=type,location=location,water_every_days=water_every_days)

