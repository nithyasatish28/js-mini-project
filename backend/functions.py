from sqlalchemy import Integer, String, Column, create_engine, DateTime, ForeignKey
from sqlalchemy.orm import Session, declarative_base
from datetime import datetime


DB_PATH = "./plants_orphange.db"
engine = create_engine(f"sqlite:///{DB_PATH}")
Base = declarative_base()

class Plants(Base):
    __tablename__ = "plants"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    type = Column(String)
    location = Column(String)
    water_every_days = Column(Integer)
    adopted_by = Column(String, nullable=True)


class Watering(Base):
    __tablename__ = "waterings"
    id = Column(Integer, primary_key=True)
    plant_id = Column(Integer, ForeignKey("plants.id"))
    roll_no = Column(String)
    watered_on = Column(DateTime , default=datetime.now())

Base.metadata.create_all(engine)


def get_all_plants(plant_type=None): #gives all plants, may be filtered with type
    session = Session(engine)
    if plant_type is None:
        plants = session.query(Plants).all()
        response = []
        for plant in plants:
            temp_plant = {
                "id": plant.id,
                "name": plant.name,
                "type": plant.type,
                "location": plant.location,
                "water_every_days": plant.water_every_days,
                "adopted_by": plant.adopted_by

            }
            response.append(temp_plant)
        session.close()
        return response
    else:
        plants = session.query(Plants).filter(Plants.type == plant_type)
        response = []
        for plant in plants:
            temp_plant = {
                "id": plant.id,
                "name": plant.name,
                "type": plant.type,
                "location": plant.location,
                "water_every_days": plant.water_every_days,
                "adopted_by": plant.adopted_by

            }
            response.append(temp_plant)
        session.close()
        return response

def get_plant(id): #gets info about specific plant from id
    session = Session(engine)
    plant = session.get(Plants, id)
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