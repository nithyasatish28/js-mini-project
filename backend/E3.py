from function import engine, Plants
from sqlalchemy.orm import Session


def add_plant(name, type, location, water_every_days):

    session = Session(engine)

    plant = Plants(
        name=name,
        type=type,
        location=location,
        water_every_days=water_every_days,
        adopted_by=None
    )

    session.add(plant)
    session.commit()
    session.refresh(plant)

    response = {
        "id": plant.id,
        "name": plant.name,
        "type": plant.type,
        "location": plant.location,
        "water_every_days": plant.water_every_days,
        "adopted_by": plant.adopted_by
    }

    session.close()
    return response