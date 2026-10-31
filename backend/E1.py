
from function import engine
from sqlalchemy import MetaData, Table


def get_all_plants(plant_type=None):
    db = engine.connect()

    plants = Table("plants", MetaData(), autoload_with=engine)
    waterings = Table("waterings", MetaData(), autoload_with=engine)

    all_plants = db.execute(plants.select()).fetchall()
    result = []

    for plant in all_plants:
        if plant_type and plant.type != plant_type:
            continue

        watering = db.execute(
            waterings.select().where(waterings.c.plant_id == plant.id)
        ).fetchall()

        last_watered = max(
            [w.watered_on for w in watering], default=None
        )

        result.append({
            "id": plant.id,
            "name": plant.name,
            "type": plant.type,
            "location": plant.location,
            "water_every_days": plant.water_every_days,
            "adopted_by": plant.adopted_by,
            "last_watered_date": last_watered
        })

    db.close()
    return result
