from function import engine, Plants, Waterings
from sqlalchemy.orm import Session
from datetime import date
from fastapi import HTTPException


def unadopt_plant(id):
    session = Session(engine)
    plant = session.get(Plants, id)
    if not plant:
        session.close()
        raise HTTPException(status_code=404, detail="Plant not found")
    if not plant.adopted_by:
        session.close()
        raise HTTPException(status_code=400, detail="Plant is not currently adopted")

    plant.adopted_by = None
    session.commit()
    response = {"id": plant.id, 
                "name": plant.name, 
                "adopted_by": plant.adopted_by}
    session.close()
    return response
        