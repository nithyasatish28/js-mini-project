from fastapi import FastAPI, HTTPException
import functions

app = FastAPI()


@app.get("/equipment")
def get_equipment():
    return functions.get_all_equipments() 

# @app.post("/equipment")
# def add_equipment(name: str, equipment_type: str, lab_room: str):

#     return functions.add_equipment(name, equipment_type, lab_room)

@app.post("/equipment")
def add_equipment(name, equipment_type, lab_room):

    if not name or not lab_room or not equipment_type:
        raise HTTPException(status_code=422, detail="All fields are required")

    if equipment_type not in functions.equipment_types:
        raise HTTPException(status_code=422, detail="Invalid equipment type")

    return functions.add_equipment(name=name,equipment_type=equipment_type,lab_room=lab_room)