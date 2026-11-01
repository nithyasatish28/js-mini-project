from sqlalchemy import Integer, String, Column, create_engine, DateTime, ForeignKey
from sqlalchemy.orm import Session, declarative_base
from datetime import datetime, date
from fastapi import HTTPException
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = "garden.db"
engine = create_engine(f"sqlite:///{DB_PATH}")
Base = declarative_base()


class Plants(Base):
    __tablename__ = "plants"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    type = Column(String)
    location = Column(String, nullable=True)
    water_every_days = Column(Integer)
    adopted_by = Column(String, nullable=True)


class Waterings(Base):
    __tablename__ = "waterings"

    id = Column(Integer, primary_key=True)
    roll_no = Column(String)
    plant_id = Column(Integer, ForeignKey("plants.id"))
    watered_on = Column(DateTime, default=datetime.now)


Base.metadata.create_all(engine)

VALID_TYPES = ["Succulent", "Flowering", "Herb", "Indoor", "Tree"]


# E1 - Get all plants
def get_all_plants(plant_type=None):

    if plant_type is not None:
        
        plant_type = plant_type.strip().capitalize()  

        if plant_type not in VALID_TYPES:
            raise HTTPException(status_code=422, detail="Invalid plant type")

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
            last_watered = watering.watered_on.isoformat()
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

    
#E2 - Get plant by id

def get_plant(id):
    session = Session(engine)
    plant = session.get(Plants, id)
    if plant is None:
        session.close()
        raise HTTPException(status_code = 404, detail = "Plant not Found")
    
    waterings = session.query(Waterings).all()
    response_water=[]
    for water in waterings:

        if water.plant_id == id:
            temp_water={
                "id": water.id,
                "roll_no": water.roll_no,         
                "watered_on": water.watered_on   
                }
            response_water.append(temp_water)        
    
    response = {
            "id": plant.id,
            "name": plant.name,
            "type": plant.type,
            "location": plant.location,
            "water_every_days": plant.water_every_days,
            "adopted_by": plant.adopted_by,
            "waterings": response_water,
           }
    session.close()
    return response

#E3 - Adopt a plant

def add_plant(name, type, location, water_every_days):
    if not name or not str(name).strip():
        raise HTTPException(status_code=422, detail="Plant name cannot be empty")
    if not location or not str(location).strip():
        raise HTTPException(status_code=422, detail="Location cannot be empty")
    if not type or str(type).strip().lower() not in VALID_TYPES:
        raise HTTPException(status_code=422, detail="Invalid plant type")
    if water_every_days is None or not (1 <= int(water_every_days) <= 14):
        raise HTTPException(status_code=422, detail="water_every_days must be between 1 and 14")

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

#E4 - Adopt a plant
def adopt_plant(plant_id, roll_no):
    if not roll_no or not str(roll_no).strip():
        raise HTTPException(status_code=422, detail="Roll number cannot be empty")

    clean_roll = str(roll_no).strip()
    session = Session(engine)
    plant = session.get(Plants, plant_id)
    
   
    if plant is None:
        session.close()
        raise HTTPException(status_code=409, detail="Plant does not exist")
        
   
    if plant.adopted_by:
        session.close()
        raise HTTPException(status_code=409, detail="Plant is already adopted")

    
    adopted_count = session.query(Plants).filter(Plants.adopted_by == clean_roll).count()
    if adopted_count >= 2:
        session.close()
        raise HTTPException(status_code=409, detail="A student cannot adopt more than 2 plants")  
      
    plant.adopted_by = clean_roll
    session.commit()
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

#E5 - Unadopt a plant
def unadopt_plant(id):
    session = Session(engine)
    plant = session.get(Plants, id)
    if not plant:
        session.close()
        raise HTTPException(status_code=404, detail="Plant not found")
    if not plant.adopted_by:
        session.close()
        raise HTTPException(status_code=400, detail="Plant is not currently adopted")

    plant.adopted_by = None
    session.commit()
    response = {"id": plant.id, 
                "name": plant.name, 
                "adopted_by": plant.adopted_by}
    session.close()
    return response

#E6 - Water a plant
def water_plant(plant_id, roll_no): 
    if not roll_no or not str(roll_no).strip():
        raise HTTPException(status_code=422, detail="Roll number cannot be empty")
    
    clean_roll = str(roll_no).strip()

    session = Session(engine)

    plant = session.get(Plants, plant_id)

    if not plant:
        session.close()
        raise HTTPException(status_code=404, detail="Plant doesn't exist")

    if plant.adopted_by != clean_roll:
        session.close()
        raise HTTPException(status_code=403, detail="only the student who adopted the plant can water it")

    last_watered = session.query(Waterings).filter(
        Waterings.plant_id == plant_id
    ).order_by(Waterings.watered_on.desc()).first()

    if last_watered and last_watered.watered_on == date.today():
        session.close()
        raise HTTPException(status_code=409, detail="Plant has already been watered today")

    watering = Waterings(
        plant_id=plant_id,
        roll_no=clean_roll,
        watered_on=datetime.now()
    )

    session.add(watering)
    session.commit()
    session.refresh(watering)

    response = {
        "id": watering.id,
        "plant_id": watering.plant_id,
        "roll_no": watering.roll_no,
        "watered_on": watering.watered_on.isoformat()
    }

    session.close()
    return response

#E7 - Get plants that need water
def get_need_water():

    session = Session(engine)

    plants = session.query(Plants).all()
    response = []

    for plant in plants:
        watering = session.query(Waterings).filter(
            Waterings.plant_id == plant.id
            ).order_by(Waterings.watered_on.desc()).first()
        
        if watering is None:
            response.append({
                "id": plant.id,
                "name": plant.name,
                "type": plant.type,
                "location": plant.location,
                "water_every_days": plant.water_every_days,
                "adopted_by": plant.adopted_by,
                "last_watered": None
            })

        elif (date.today() - watering.watered_on.date()).days >= plant.water_every_days:

            response.append {
                "id": plant.id,
                "name": plant.name,
                "type": plant.type,
                "location": plant.location,
                "water_every_days": plant.water_every_days,
                "adopted_by": plant.adopted_by,
                "last_watered": watering.watered_on.isoformat()
            }

            

    session.close()
    return response
