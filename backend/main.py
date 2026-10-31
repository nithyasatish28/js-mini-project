from fastapi import FastAPI, HTTPException, Body, Query
from fastapi.middleware.cors import CORSMiddleware
import function

app = FastAPI(title="Laboratory Equipment Booking System")

app.add_middleware(
    _import_("fastapi").middleware.cors.CORSMiddleware,
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


@app.get("/equipment/{id}")
def equipment_by_id(id: int):
    result = function.get_equipment(id)
    if result is None:
        raise HTTPException(status_code=404,detail="Equipment not found.")
    return result


@app.post("/equipment", status_code=201)
def add_equipment(name: str = Body(...),type: str = Body(...),lab_room: str = Body(...)):
    if not name.strip() or not lab_room.strip():
        raise HTTPException(status_code=422,detail="Name and lab room cannot be empty.")
    if type not in function.VALID_TYPES:
        raise HTTPException(status_code=422,detail="Invalid equipment type.")
    return function.add_equipment(name=name, type=type, lab_room=lab_room)