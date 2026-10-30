from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import functions


app = FastAPI()

app.add_middleware(CORSMiddleware,
                   allow_origins=["http://localhost:5173"],
                   allow_methods=["*"],
                   allow_headers=["*"])


@app.get("/plants")
def plants(plant_type=None):
    return functions.get_all_plants(plant_type=plant_type)

