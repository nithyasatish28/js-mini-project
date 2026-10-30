
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import Session, declarative_base
from datetime import datetime

DB_PATH = "garden.db"
engine = create_engine(f"sqlite:///{DB_PATH}")
Base = declarative_base()


class Plants(Base):
    __tablename__ = "Plants"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    type = Column(String)
    water_every_days = Column(Integer)
    location = Column(String, nullable=True)
    adopted_by = Column(String, nullable=True)


class Waterings(Base):
    __tablename__ = "waterings"

    id = Column(Integer, primary_key=True)
    plant_id = Column(Integer, ForeignKey("Plants.id"))
    roll_no = Column(String)
    watered_on = Column(DateTime, default=datetime.now)


Base.metadata.create_all(engine)


# E3 - Add a plant
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


# E1 - Get all plants
def get_all_plants(type=None):

    session = Session(engine)

    query = session.query(Plants)

    if type:
        query = query.filter(Plants.type == type)

    plants = query.all()

    response = []

    for plant in plants:

        last_watering = session.query(Waterings).filter(
            Waterings.plant_id == plant.id
        ).order_by(Waterings.watered_on.desc()).first()

        temp_plant = {
            "id": plant.id,
            "name": plant.name,
            "type": plant.type,
            "location": plant.location,
            "water_every_days": plant.water_every_days,
            "adopted_by": plant.adopted_by,
            "last_watered": (
                last_watering.watered_on.date().isoformat()
                if last_watering else None
            )
        }

        response.append(temp_plant)

    session.close()
    return response


# E2 - Get one plant and its waterings
def get_waterings(plant_id):

    session = Session(engine)

    plant = session.get(Plants, plant_id)

    if plant is None:
        session.close()
        return None

    waterings = session.query(Waterings).filter(
        Waterings.plant_id == plant_id
    ).order_by(Waterings.watered_on.desc()).all()

    response = {
        "id": plant.id,
        "name": plant.name,
        "type": plant.type,
        "location": plant.location,
        "water_every_days": plant.water_every_days,
        "adopted_by": plant.adopted_by,
        "waterings": []
    }

    for watering in waterings:
        response["waterings"].append({
            "id": watering.id,
            "plant_id": watering.plant_id,
            "roll_no": watering.roll_no,
            "watered_on": watering.watered_on.isoformat()
        })

    session.close()
    return response
