from sqlalchemy import Integer, String, Column, create_engine, DateTime, ForeignKey
from sqlalchemy.orm import Session, declarative_base
from datetime import datetime, date
from fastapi import HTTPException



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


# E1 - Get all plants
def get_all_plants(plant_type=None):

    if plant_type is not None:
        
        plant_type = plant_type.strip()
        # .capitalize()  

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

    
#E2 - Get plant by id

def get_plant(id):
    session = Session(engine)
    plant = session.get(Plants, id)
    if plant is None:
        session.close()
        raise HTTPException(status_code = 404, detail = "Item id not in the menu")
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
    return response,response_water

#E3 - Adopt a plant

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

#E4 - Adopt a plant
def adopt_plant(plant_id, roll_no):
    session = Session(engine)
    plant = session.get(Plants, plant_id)
    
   
    if plant is None:
        session.close()
        raise HTTPException(status_code=404, detail="Plant doesnt exist")
        
   
    if plant.adopted_by:
        session.close()
        raise HTTPException(status_code=409, detail="Plant is already adopted")
        
    plant.adopted_by = roll_no
    session.commit()
    session.close()
    return plant

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

    session = Session(engine)

    plant = session.get(Plants, plant_id)

    if not plant:
        session.close()
        raise HTTPException(status_code=404, detail="Plant doesn't exist")

    if plant.adopted_by != roll_no:
        session.close()
        raise HTTPException(status_code=403, detail="Plant is not adopted by you")

    last_watered = session.query(Waterings).filter(
        Waterings.plant_id == plant_id
    ).order_by(Waterings.watered_on.desc()).first()

    if last_watered and last_watered.watered_on == date.today():
        session.close()
        raise HTTPException(status_code=409, detail="Plant has already been watered today")

    watering = Waterings(
        plant_id=plant_id,
        roll_no=roll_no
    )

    session.add(watering)
    session.commit()
    session.refresh(watering)

    response = {
        "id": watering.id,
        "plant_id": watering.plant_id,
        "roll_no": watering.roll_no,
        "watered_on": watering.watered_on
    }

    session.close()
    return response

#E7 - Get plants that need water
def get_need_water():

    session = Session(engine)

    plants = session.query(Plants).all()
    response = []

    for plant in plants:

        last_watered = session.query(Waterings).filter(
            Waterings.plant_id == plant.id
        ).order_by(Waterings.watered_on.desc()).first()

        if last_watered is None:
            response.append({
                "id": plant.id,
                "name": plant.name,
                "type": plant.type,
                "location": plant.location,
                "water_every_days": plant.water_every_days,
                "adopted_by": plant.adopted_by,
                "last_watered": None
            })

        elif (date.today() - last_watered.watered_on).days >= plant.water_every_days:

            temp_plant = {
                "id": plant.id,
                "name": plant.name,
                "type": plant.type,
                "location": plant.location,
                "water_every_days": plant.water_every_days,
                "adopted_by": plant.adopted_by,
                "last_watered": last_watered.watered_on
            }

            response.append(temp_plant)

    session.close()
    return response
