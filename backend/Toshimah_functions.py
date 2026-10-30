from sqlalchemy import Integer, String, DateTime, Column, ForeignKey, create_engine, Boolean;
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
    adopted_by = Column(Boolean, nullable=True)
    
   

class waterings(Base):
    __tablename__="waterings"
    id = Column(Integer, primary_key=True)
    plant_id = Column(Integer, ForeignKey("plants.id"))
    roll_no = Column(Integer) 
    watered_on = Column(DateTime)
    
    
    
Base.metadata.create_all(engine)



def seed_data():
    session = Session(engine)
    if session.query(plants).count() == 0:
        plant_records = [
            plants(id=1, name="Tulsi", type="herb", location="Block A garden", water_every_days=2, adopted_by=True),
            plants(id=2, name="Aloe Vera", type="succulent", location="Library window", water_every_days=10, adopted_by=True),
            plants(id=3, name="Rose", type="flowering", location="Main gate", water_every_days=2, adopted_by=True),
            plants(id=4, name="Money Plant", type="indoor", location="Admin office", water_every_days=5, adopted_by=True),
            plants(id=5, name="Neem", type="tree", location="Canteen", water_every_days=7, adopted_by=True),
            plants(id=6, name="Mint", type="herb", location="Hostel terrace", water_every_days=1, adopted_by=True),
            plants(id=7, name="Jade Plant", type="succulent", location="Lab 3", water_every_days=14, adopted_by=False),
            plants(id=8, name="Hibiscus", type="flowering", location="Block B entrance", water_every_days=3, adopted_by=False),
            plants(id=9, name="Snake Plant", type="indoor", location="Reception", water_every_days=10, adopted_by=False),
            plants(id=10, name="Mango", type="tree", location="Sports ground", water_every_days=7, adopted_by=False),
        ]
        session.add_all(plant_records)
        session.commit()
    if session.query(waterings).count() == 0:
        watering_records = [
            waterings(plant_id=1, roll_no=101, watered_on=datetime.now()),
            waterings(plant_id=2, roll_no=102, watered_on=datetime.now()),
            waterings(plant_id=3, roll_no=103, watered_on=datetime.now()),
        ]
        session.add_all(watering_records)
        session.commit()
    session.close()
        
        
seed_data()


def add_plant(name, type, location, water_every_days):
    session = Session(engine)
    plant = plants(name = name , type= type , location = location ,  water_every_days = water_every_days, adopted_by = True)
    session.add(plant)
    session.commit()
    session.refresh(plant)
    response = {
        "id" : plant.id,
        "name" : plant.name,
        "type" : plant.type,
        "location" : plant.location,
        "water_every_days" : plant.water_every_days,
        "adopted_by" : plant.adopted_by
    }
    session.close()
    return response

def unadopt_plant(id):
    session = Session(engine)
    plant = session.get(plants, id)
    if not plant:
        session.close()
        raise HTTPException(status_code=404, detail="Plant not found")
    if plant.adopted_by == False:
        session.close()
        raise HTTPException(status_code=400, detail="Plant is not currently adopted")

    plant.adopted_by = False
    session.commit()
    response = {"id": plant.id, "name": plant.name, "adopted_by": plant.adopted_by}
    session.close()
    return response
        
def water_plant(id, roll_no):
    session = Session(engine)
    plant = session.get(plants, id)
    if not plant:
        session.close()
        raise HTTPException(status_code=404, detail="Plant not found")
    
    watered_on = datetime.now()
    watering = waterings(plant_id=id, roll_no=roll_no, watered_on=watered_on)
    session.add(watering)
    session.commit()
    session.refresh(watering)
    response = {"id": watering.id, "plant_id": watering.plant_id,
        "roll_no": watering.roll_no, "watered_on": watering.watered_on}
    session.close()

    return response

    
    


 