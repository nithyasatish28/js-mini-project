

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
    roll_no = Column(Integer)
    watered_on = Column(DateTime, default=datetime.now) 

Base.metadata.create_all(engine)

def add_plant(id,name,type,water_every_days,adopted_by = bool,location = None):
    session = Session(engine)
    plant = Plants(id = id,name=name,type =type,water_every_days = water_every_days,adopted_by = adopted_by,location= location) 
    session.add(Plants)
    response = {
        "id": Plants.id,
        "name":Plants.name,
        "type":Plants.type,
        "water_every_days": Plants.water_every_days,
        "location":  Plants.location,
        "adopted_by":  Plants.adopted_by
        
    }
    session.commit() 
    session.close()
    return response


def add_waterings(id,plant_id,roll_no,watered_on):
    session = Session(engine)
    Watering = Waterings(id =id,plant_id = plant_id,roll_no= roll_no,watered_on = watered_on)
    session.add(Waterings)
    response = {
        "id": Waterings.id,
        "plant_id":Waterings.plant_id,
        "roll_no":Waterings.roll_no,
        "watered_on":Waterings.watered_on
    }
    session.commit() 
    session.close()
    return response

def get_all_Plants():
    session = Session(engine)
    Plants = session.query(Plants).all()
    response = []
    for plant in Plants:
        temp_plant = {
            "id": plant.id,
            "name":plant.name,
            "type":plant.type,
            "water_every_days": plant.water_every_days,
            "location":  plant.location,
            "adopted_by":  plant.adopted_by
           
        }

        response.append(temp_plant)
    session.close()
    return response

def get_all_Waterings():
    session = Session(engine)
    Waterings = session.query(Waterings).all()
    response =[]
    for watering in Waterings:
        temp_watering = {
            "id": watering.id,
            "plant_id": watering.plant_id,
            "roll_no": watering.roll_no,
            "watered-on":watering.watered_on
        }
        response.append(temp_watering)
    session.close()
    return response

    