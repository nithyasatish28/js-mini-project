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
def plants(type: str = None):
    return functions.get_all_plants(type=type)

@app.get("/plants/{plant_id}")
def plant(plant_id: int):
    return functions.get_waterings(plant_id = plant_id)


from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import functions

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
def hello():
    return {"message": "Garden API is running"}


# E1 - Get all plants
@app.get("/plants")
def plants(type: str = None):
    return functions.get_all_plants(type=type)


# E2 - Get one plant with watering history
@app.get("/plants/{plant_id}")
def plant(plant_id: int):

    result = functions.get_waterings(plant_id)
    if result is None:raise HTTPException(status_code=404,detail="Plant not found")
    return result


# E3 - Add a new plant
@app.post("/plants")
def add_plant(name: str,type: str,water_every_days: int,location: str = None):
    allowed_types = ["succulent","flowering","herb","indoor","tree" ]
    if not name.strip():raise HTTPException(status_code=422,detail="Name is required")
    if type not in allowed_types:raise HTTPException(status_code=422,detail="Invalid plant type")
    if water_every_days < 1 or water_every_days > 14:raise HTTPException(status_code=422,detail="Watering days must be between 1 and 14")

    return functions.add_plant(name=name,type=type,location=location,water_every_days=water_every_days)

