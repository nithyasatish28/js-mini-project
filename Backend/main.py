from fastapi import FastAPI,HTTPException
from Backend import E1
app=FastAPI()
@app.get("/equipment")
def get_equipment():
    return E1.get_all_equipment()

@app.get("/equipment/{equipment_type}")
def get_equipment_by_type(equipment_type: str):
    return E1.get_equipment_by_type(equipment_type)