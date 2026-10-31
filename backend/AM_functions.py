from sqlalchemy import Integer, String, Column, create_engine,ForeignKey, DateTime
from sqlalchemy.orm import Session, declarative_base;

from datetime import date;


from fastapi import HTTPException;

DB_PATH = "garden.db"

engine = create_engine(f"sqlite:///{DB_PATH}")
Base = declarative_base()


class Plants(Base):
    __tablename__="plants"

    id = Column(Integer,primary_key = True)
    name = Column(String)
    type = Column(String)
    location = Column(String,nullable = True)
    water_every_days = Column(Integer)
    adopted_by = Column(String,default = None)
    
   

class Waterings(Base):
    __tablename__="waterings"
    
    id = Column(Integer,primary_key = True)
    plant_id = Column(Integer, ForeignKey("plants.id"))
    roll_no = Column(String)
    watered_on= Column(DateTime)
    
    
Base.metadata.create_all(engine)


# E1-get all info of plants
def get_all_plants(type = None):
    
    if type is not None :
            type = type.strip().lower().strip("")
            if type not in ["succulent", "flowering", "herb", "indoor", "tree"]:
                raise HTTPException(status_code=404, detail="Invalid plant type")

    session = Session(engine)
    plant_query = session.query(Plants)    

    if type is not None:
        plant_query = plant_query.filter(Plants.type == type)     
    plants = plant_query.all()
    
            
    response = []

    for plant in plants:
        
        latest = session.query(Waterings).filter(Waterings.plant_id == plant.id).order_by(Waterings.watered_on.desc()).first()
        last_watered = None
        need_water = True
        if latest is not None:
            last_watered = latest.watered_on
            
            days = (date.today() - last_watered.date()).days
            
            need_water = days >= plant.water_every_days
        temp_plant ={
            "id": plant.id,
           "name": plant.name,
            "type": plant.type,
            "location": plant.location,
            "adopted_by":plant.adopted_by,
            "water_every_days":plant.water_every_days,
            "last_watered": last_watered,
            "need_water": need_water,
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


# E4-adpot by roll number
def adopt_plant(id,roll_no):
    session = Session(engine)
    plant = session.get(Plants, id)
    
    if plant is None:
        session.close()
        raise HTTPException(status_code = 404, detail = "Plant Not Found")

    if plant.adopted_by:
        session.close()
        raise HTTPException(status_code = 409, detail = "Plant already adpoted")

    count = session.query(Plants).filter(Plants.adopted_by == roll_no).count()
    print("Adopted plants count:", count)
    if count >= 2: 
        session.close()
        raise HTTPException(status_code = 409, detail = "can adopt at most 2 plants")

    plant.adopted_by = roll_no
    session.commit()
    session.close()
    
    return get_plant(id)


#E7 plants that need water
def get_need_water():
    plants = get_all_plants()
    response = []
    for plant in plants:
        if plant["need_water"]:
            response.append(plant)
    return response