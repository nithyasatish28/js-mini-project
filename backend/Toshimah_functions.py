from sqlalchemy import Integer, String, DateTime,Column, create_engine;
from sqlalchemy.orm import Session, declarative_base;
from datetime import datetime;
from fastapi import FastAPI, HTTPException
import AM_functions;

DB_PATH = "garden.db"

engine = create_engine(f"sqlite:///{DB_PATH}")
Base = declarative_base()

class plants(Base):
    __tablename__="plants"

    id = Column(Integer,primary_key = True)
    name = Column(String)
    type = Column(String)
    location = Column(String,nullable = True)
    water_every_days = Column(Integer)
    adopted_by = Column(String,nullable = True)
    
   


class waterings(Base):
    __tablename__="waterings"
    
    id = Column(Integer,primary_key = True)
    plant_id = Column(Integer, Foreign_Key=plants.id)
    roll_no = Column(String)
    watered_on= Column(String)
    
    
    
Base.metadata.create_all(engine)



def seed_data():
    session = session(engine)
    if session.query(plants).count() == 0:
        plants[
            plants(name="Tulsi", type="herb", location="Block A garden", water_every_days=2, adopted_by="21CS001"),
            plants(name="Aloe Vera", type="succulent", location="Library window", water_every_days=10, adopted_by="21CS002"),
            plants(name="Rose", type="flowering", location="Main gate", water_every_days=2, adopted_by="21CS003"),
            plants(name="Money Plant", type="indoor", location="Admin office", water_every_days=5, adopted_by="21CS001"),
            plants(name="Neem", type="tree", location="Canteen", water_every_days=7, adopted_by="21CS004"),
            plants(name="Mint", type="herb", location="Hostel terrace", water_every_days=1, adopted_by="21CS005"),
            plants(name="Jade Plant", type="succulent", location="Lab 3", water_every_days=14),
            plants(name="Hibiscus", type="flowering", location="Block B entrance", water_every_days=3),
            plants(name="Snake Plant", type="indoor", location="Reception", water_every_days=10),
            plants(name="Mango", type="tree", location="Sports ground", water_every_days=7),
        ]
        session.add_all(plants)
        session.commit()
        
        
def add_plant(name, type, location, water_every_days, adopted_by):
    session = session(engine)
    plant = plants(name = name , type= type , location = location ,  water_every_days = water_every_days, adopted_by = True)
    session.add(plant)
    response = {
        "id" : plant.id,
        "name" : plant.name,
        "type" : plant.type,
        "location" : plant.location,
        "water_every_days" : plant.water_every_days,
        "adopted_by" : plant.adopted_by
    }
    session.commit()
    session.close()
    return response

def unadopt_plant(id):
    session = Session(engine)
    plant = session.get( id)
    if not plant:
        session.close()
        raise HTTPException(status_code=404, detail="Plant not found")
    if not plant.adopted_by:
        session.close()
        raise HTTPException(status_code=400, detail="Plant is not currently adopted")

    plant.adopted_by = None
    session.commit()
    session.close()
    return {"id": plant.id, "name": plant.name, "adopted_by": False}

        
def water_plant(id, roll_no):
    session = Session(engine)
    plant = session.get(id)
    if not plant:
        session.close()
        raise HTTPException(status_code=404, detail="Plant not found")
    
    watering = waterings(plant_id=id, roll_no=roll_no, watered_on= datetime)
    session.add(watering)
    session.commit()
    session.refresh(watering)
    session.close()
    
    return {"id": watering.id, "plant_id": watering.plant_id, 
            "roll_no": watering.roll_no, "watered_on": datetime}
  
    
    


 