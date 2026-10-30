from sqlalchemy import Integer, String, Column, create_engine,inspect,ForeignKey,DateTime, Boolean
from sqlalchemy.orm import Session, declarative_base;

from datetime import datetime;

DB_PATH = "garden.db"

engine = create_engine(f"sqlite:///{DB_PATH}")
Base = declarative_base()
print(inspect(engine).get_table_names())

class Plants(Base):
    __tablename__="plants"

    id = Column(Integer,primary_key = True)
    name = Column(String)
    type = Column(String)
    location = Column(String,nullable = True)
    water_every_days = Column(Integer)
    adopted_by = Column(Boolean,default = False)
    
   

class Waterings(Base):
    __tablename__="waterings"
    
    id = Column(Integer,primary_key = True)
    plant_id = Column(Integer, ForeignKey("plants.id"))
    roll_no = Column(Integer)
    watered_on= Column(DateTime)
    
    
Base.metadata.create_all(engine)


# E1-get all info of plants
def get_all_plants(type = None):
    
    session = Session(engine)
    plant_query = session.query(Plants)
    if type is not None:
        plant_query = plant_query.filter(Plants.type == type)
    plants = plant_query.all()
    last_watered = None
    waterrings = session.query(Waterings).all()
    for watering in waterrings:
        if watering.plant_id == plant.id:
            last_watered = watering.watered_on
            
    response = []
    for plant in plants:
        temp_plant ={
            "id": plant.id,
            "name": plant.name,
            "type": plant.type,
            "location": plant.location,
            "last_watered": last_watered
             }
        response.append(temp_plant)
    session.close()
    return response 

#E2-get a plant by its id
def get_plant(id):
    session = Session(engine)
    plant = session.get(Plants, id)
    if plant is None:
        session.close()
        
    else:
        response = {
                "id": plant.id,
                "name": plant.name,
                "type": plant.type,
                "location": plant.location,
                "water_every_days": plant.water_every_days,
                "adopted_by": plant.adopted_by
            }
        waterings = session.query(Waterings).all()
        response_water=[]
        for water in waterings:
            temp_water={
                "id": water.id,
                "roll_no": water.roll_no,
                "watered_on": water.watered_on   
            }
            response_water.append(temp_water)     
        session.close()
        return response


# E4-adpot by roll number
def adpot_plant(id,roll_no):
    session = Session(engine)
    plant = session.get(Plants, id)
    return