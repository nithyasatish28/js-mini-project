from fastapi import FastAPI, HTTPException
from datetime import date
import functions

app = FastAPI()


@app.get("/equipment")
def get_equipment():
    return functions.get_all_equipments() 

@app.get("/equipment/type/{equipment_type}")
def get_equipment_by_type(equipment_type: str):
    return functions.get_equipment_by_type(equipment_type)

@app.get("/equipment/{equipment_id}")
def equipment_by_id(equipment_id: int):

    if functions.get_equipment_by_id(equipment_id=equipment_id) is None:
        raise HTTPException(status_code=404, detail="Equipment not found")

    return functions.get_equipment_by_id(equipment_id=equipment_id)


@app.post("/equipment")
def add_equipment(name, equipment_type, lab_room):

    if not name or not lab_room or not equipment_type:
        raise HTTPException(status_code=422, detail="All fields are required")

    if equipment_type not in functions.equipment_types:
        raise HTTPException(status_code=422, detail="Invalid equipment type")

    return functions.add_equipment(name=name,equipment_type=equipment_type,lab_room=lab_room)

