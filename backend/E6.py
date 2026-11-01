from function import engine, Plants, Waterings
from sqlalchemy.orm import Session
from datetime import date
from fastapi import HTTPException


def water_plant(plant_id, roll_no):  

    session = Session(engine)

    plant = session.get(Plants, plant_id)

    if not plant:
        session.close()
        raise HTTPException(status_code=404, detail="Plant doesn't exist")

    if plant.adopted_by != roll_no:
        session.close()
        raise HTTPException(status_code=403, detail="Plant is not adopted by you")

    last_watered = session.query(Waterings).filter(
        Waterings.plant_id == plant_id
    ).order_by(Waterings.watered_on.desc()).first()

    if last_watered and last_watered.watered_on == date.today():
        session.close()
        raise HTTPException(status_code=409, detail="Plant has already been watered today")

    watering = Waterings(
        plant_id=plant_id,
        roll_no=roll_no
    )

    session.add(watering)
    session.commit()
    session.refresh(watering)

    response = {
        "id": watering.id,
        "plant_id": watering.plant_id,
        "roll_no": watering.roll_no,
        "watered_on": watering.watered_on
    }

    session.close()
    return response