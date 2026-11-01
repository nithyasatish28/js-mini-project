from datetime import date
from sqlalchemy.orm import Session
from function import engine, Plants, Waterings
from fastapi import HTTPException


def get_all_plants(plant_type=None):

    if plant_type is not None:
        # .lower=.capitalize()
        plant_type = plant_type.strip().lower()  

        if plant_type not in ["succulent", "flowering", "herb", "indoor", "tree"]:
            raise HTTPException(status_code=404, detail="Invalid plant type")

    # "Session" and "Engine" used to connect and communicate with database using SQLALCHEMY.
    # "Engine" is responsible for managing the database connection.
    session = Session(engine)

    plant_query = session.query(Plants)

    if plant_type is not None:
        plant_query = plant_query.filter(Plants.type == plant_type)

    all_plants = plant_query.all()
    result = []

    for plant in all_plants:

        watering = session.query(Waterings).filter(
            Waterings.plant_id == plant.id
        ).order_by(Waterings.watered_on.desc()).first()

        last_watered = None
        need_water = True

        if watering is not None:
            last_watered = watering.watered_on
            days = (date.today() - last_watered.date()).days
            need_water = days >= plant.water_every_days

        result.append({
            "id": plant.id,
            "name": plant.name,
            "type": plant.type,
            "location": plant.location,
            "water_every_days": plant.water_every_days,
            "adopted_by": plant.adopted_by,
            "last_watered": last_watered,
            "need_water": need_water
        })

    session.close()
    return result

def add_plant(name, type, location, water_every_days):

    session = Session(engine)

    new_plant = Plants(
        name=name,
        type=type,
        location=location,
        water_every_days=water_every_days
    )

    session.add(new_plant)
    session.commit()
    session.refresh(new_plant)

    result = {
        "id": new_plant.id,
        "name": new_plant.name,
        "type": new_plant.type,
        "location": new_plant.location,
        "water_every_days": new_plant.water_every_days,
        "adopted_by": new_plant.adopted_by
    }

    session.close()
    return result