from fastapi import FastAPI , HTTPException
import functions

app=FastAPI()

@app.get("/plants")
def plants():
    return functions.get_all_plants()


@app.get("/plants/{id}")
def plants_by_id(id):
    # return functions.get_all_plants(id=id)
    plant=functions.get_all_plants(id=id)
    if plant is None:
        raise HTTPException(status_code=404,detail="plant not found")
    return plant


@app.post("/plants")
def plants_new(name,type,location,water_every_days):
    allowed_type = ["succulent","flowering","herb","indoor","tree"]
    if type is not in allowed_type:
        raise HTTPException(status_code=422,detail="invalid type ")

    return functions.get_all_plants(name=name,type=type,location=location,water_every_days=water_every_days)
    

@app.post("/waterings/plants")
def plants_adopt(roll_no,plant_id):  
    return functions.get_all_plants(roll_no=roll_no,plant_id=plant_id)

@app.patch("/plants/{id}")
def plants_not_adopted(plant_id):
    return functions.get_all_plants(plant_id=plant_id)

@app.post("/waterings/{plant_id}")
def plants_log(plant_id,roll_no,watered_on):
    return functions.get_all_plants(plant_id=plant_id,roll_no=roll_no,watered_on=watered_on)

@app.get("/plants/want_water")
def plants_today(id,water_every_days):
    return functions.get_all_plants(id=id,water_every_days=water_every_days)

