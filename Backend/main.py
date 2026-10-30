from fastapi import FastAPI,HTTPException
from Backend import E1
from Backend import E2



app=FastAPI()

# E1 - Get all equipment
@app.get("/equipment")
def get_equipment():
    return E1.get_all_equipment()

# E1 - Get equipment by type
@app.get("/equipment/type/{equipment_type}")
def get_equipment_by_type(equipment_type: str):
    return E1.get_equipment_by_type(equipment_type)

# E2 - Get equipment by ID
@app.get("/equipment/{equipment_id}")
def get_equipment_by_id(equipment_id: int):
    equipment = E2.get_equipment_by_id(equipment_id)

    if equipment is None:
        raise HTTPException(status_code=404, detail="Equipment not found")

    return equipment