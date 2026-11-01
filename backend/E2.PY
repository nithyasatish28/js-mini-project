from datetime import date
from sqlalchemy.orm import Session
from function import engine, Plants, Waterings
from fastapi import HTTPException


def get_plant(id):
    session = Session(engine)
    plant = session.get(Plants, id)
    if plant is None:
        session.close()
        raise HTTPException(status_code = 404, detail = "Item id not in the menu")
    waterings = session.query(Waterings).all()
    response_water=[]
    for water in waterings:

        if water.plant_id == id:
            temp_water={
                "id": water.id,
                "roll_no": water.roll_no,
                "watered_on": water.watered_on   
                }
            response_water.append(temp_water)        
    
    response = {
            "id": plant.id,
            "name": plant.name,
            "type": plant.type,
            "location": plant.location,
            "water_every_days": plant.water_every_days,
            "adopted_by": plant.adopted_by,
            "waterings": response_water,
           }
    session.close()
    return response,response_water
