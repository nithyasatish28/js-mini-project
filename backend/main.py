from fastapi import FastAPI, HTTPException, Body, Query
from fastapi.middleware.cors import CORSMiddleware
import function

app = FastAPI(title="Laboratory Equipment Booking System")

app.add_middleware(
    __import__("fastapi").middleware.cors.CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/equipment")
def equipment(type: str = None):
    if type is not None and type not in function.VALID_TYPES:
        raise HTTPException(status_code=422,detail="Invalid equipment type.")
    return function.get_all_equipment(type=type)
