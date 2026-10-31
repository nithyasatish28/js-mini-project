from fastapi import FastAPI,HTTPException
from fastapi.middleware.cors import CORSMiddleware
import E1

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4001", "http://127.0.0.1:4001"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def hello():
    return {"message": "hello peoples"}

@app.get("/plants")
def read_plants(type: str = None):
    plants = E1.get_all_plants(type)
    return plants
