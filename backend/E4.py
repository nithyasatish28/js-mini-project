from datetime import date
from sqlalchemy.orm import Session
from function import engine, Plants, Waterings
from fastapi import HTTPException

def adopt_plant(plant_id, roll_no):
    session = Session(engine)
    plant = session.get(Plants, plant_id)
    
   
    if plant is None:
        session.close()
        raise HTTPException(status_code=404, detail="Plant doesnt exist")
        
   
    if plant.adopted_by:
        session.close()
        raise HTTPException(status_code=409, detail="Plant is already adopted")
        
    plant.adopted_by = roll_no
    session.commit()
    session.close()
    return plant