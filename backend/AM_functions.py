from sqlalchemy import Integer, String, Column, create_engine,inspect
from sqlalchemy.orm import Session, declarative_base;
from datetime import datetime;

DB_PATH = "garden.db"

engine = create_engine(f"sqlite:///{DB_PATH}")
Base = declarative_base()
print(inspect(engine).get_table_names())

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

def get_all_plants():
    session = Session(engine)
    plants = session.query(plants).all()
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


 