from http.client import HTTPException

from sqlalchemy import Integer, String, Column, create_engine,inspect,ForeignKey
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


# get all plants
def get_all_plants():
    
    session = Session(engine)
    plants = session.query(Plants).all()
    response = []
    for plant in plants:
        temp_plant ={
            "id": plant.id,
            "name": plant.name,
            "type": plant.type,
            "location": plant.location,    
             }
        response.append(temp_plant)
    session.close()
    return response 


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
        session.close()
        return response
