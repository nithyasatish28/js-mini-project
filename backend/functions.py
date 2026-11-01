

from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import Session, declarative_base
from datetime import date

DB_PATH = "garden.db"
engine = create_engine(f"sqlite:///{DB_PATH}")
Base = declarative_base()

class Plants(Base):
    __tablename__ = "plants"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    type = Column(String)
    water_every_days = Column(Integer)
    location = Column(String, nullable=True)
    adopted_by = Column(String, nullable=True)

class Waterings(Base):
    __tablename__ = "waterings" 
    id = Column(Integer, primary_key=True) 
    plant_id = Column(Integer, ForeignKey("plants.id")) 
    roll_no = Column(String)
    watered_on = Column(Date, default=date.today) 

Base.metadata.create_all(engine)


# 1)add a plant
def add_plant(name,type,water_every_days,adopted_by = None,location = None):
    session = Session(engine)
    plant = Plants(name=name,type =type,water_every_days = water_every_days,adopted_by = adopted_by,location= location) 
    session.add(plant)
    response = {
        "id": plant.id,
        "name":plant.name,
        "type":plant.type,
        "water_every_days": plant.water_every_days,
        "location":  plant.location,
        "adopted_by":  plant.adopted_by
        
    }
    session.commit() 
    session.close()
    return response



# 2)add waterings
def add_waterings(plant_id,roll_no,watered_on):
    session = Session(engine)
    Watering = Waterings(plant_id = plant_id,roll_no= roll_no,watered_on = watered_on)
    session.add(Watering)
    response = {
        "id": Watering.id,
        "plant_id":Watering.plant_id,
        "roll_no":Watering.roll_no,
        "watered_on":Watering.watered_on
    }
    session.commit() 
    session.close()
    return response


# 3)get all plants
def get_all_plants():
    session = Session(engine)
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



# 4)getting a plant by id
def get_plant_by_id(plant_id):
    session = Session(engine)
    plant = session.get(Plants, plant_id) 
    session.close()
    if plant is None:
        session.close()
        return None

    response = {
        "id": plant.id,
        "name": plant.name,
        "type": plant.type,
        "water_every_days": plant.water_every_days,
        "location": plant.location,
        "adopted_by": plant.adopted_by
    }
    session.close()
    return response


# 5)Adopting a plant
def adopt_plant(plant_id, roll_no):
    session = Session(engine)
    plant = session.get(Plants, plant_id)

    plant.adopted_by = roll_no
    if plant is None:
        return None
    response = {
        "id": plant.id,
        "adopted_by": plant.adopted_by
    }

    session.commit()
    session.close()
    return response

# 6)Giving up a plant
def give_up_plant(plant_id):
    session = Session(engine)
    plant = session.get(Plants, plant_id)
    plant.adopted_by = None

    if plant is None:
        return None
    response = {
        "id": plant.id,
        "adopted_by": plant.adopted_by
    }

    session.commit()
    session.close()
    return response


# Needs a water to a plant

def plants_need_water():
    session = Session(engine)
    plants = session.query(Plants).all()
    response = []
    for plant in plants:
        last_watered = (
            session.query(Waterings)
            .filter(Waterings.plant_id == plant.id)
            .order_by(Waterings.watered_on.desc())
            .first()
)
        

        if last_watered is None:
            need_water = True
        else:
            days = (date.today() - last_watered.watered_on).days
            need_water = days >= plant.water_every_days
        
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








