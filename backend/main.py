from fastapi import FastAPI , HTTPException
from fastapi.middleware.cors import CORSMiddleware
import functions

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173","http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/") # @ is a decorator
def hello():
    return {"message": "Hello"}

@app.get("/plants")
def plants():
    return functions.get_all_plants()

@app.get("/waterings/{plant_id}")
def plant(plant_id):
    return functions.get_waterings(plant_id = plant_id)

@app.post("/plants")
def add_plant(plant_id: int,name:str,type:str,location: None,water_every_days: int , adopted: bool=False):
    if water_every_days <=0 :
         raise HTTPException(status_code=422, detail="invalid days")
    return functions.add_plant(plant_id= plant_id ,name=name,type=type,location=location,water_every_days= water_every_days,adopted=adopted)

