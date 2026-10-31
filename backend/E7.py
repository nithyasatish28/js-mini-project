from function import engine, Plants, Waterings
from sqlalchemy.orm import Session
from datetime import date


def get_need_water():

    session = Session(engine)

    plants = session.query(Plants).all()
    response = []

    for plant in plants:

        last_watered = session.query(Waterings).filter(
            Waterings.plant_id == plant.id
        ).order_by(Waterings.watered_on.desc()).first()

        if last_watered is None:
            response.append({
                "id": plant.id,
                "name": plant.name,
                "type": plant.type,
                "location": plant.location,
                "water_every_days": plant.water_every_days,
                "adopted_by": plant.adopted_by,
                "last_watered": None
            })

        elif (date.today() - last_watered.watered_on).days >= plant.water_every_days:

            temp_plant = {
                "id": plant.id,
                "name": plant.name,
                "type": plant.type,
                "location": plant.location,
                "water_every_days": plant.water_every_days,
                "adopted_by": plant.adopted_by,
                "last_watered": last_watered.watered_on
            }

            response.append(temp_plant)

    session.close()
    return response