

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

class Watering(Base):
    __tablename__ = "watering" 
    id = Column(Integer, primary_key=True) 
    plant_id = Column(Integer, ForeignKey("Plants.id")) 
    roll_no = Column(Integer)
    watered_on = Column(DateTime, default=datetime.now) 

Base.metadata.create_all(engine)

def add_plant(name, description,contact, location = None):
    session = Session(engine)
    item = Plants(name=name, description=description, contact=contact, location=location, status="active") 
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

def get_all_items():
    session = Session(engine)
    Plants = session.query(Plants).all()
    response = []
    for plant in Plants:
        temp_item = {
            "id": plant.id,
            "name":plant.name,
            "type":plant.type,
            "water_every_days": plant.water_every_days,
            "location":  plant.location,
            "adopted_by":  plant.adopted_by
           
        }

        response.append(temp_item)
    session.close()
    return response

    