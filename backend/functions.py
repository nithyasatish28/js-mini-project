from sqlalchemy import Integer, String, Column, create_engine, DateTime, ForeignKey
from sqlalchemy.orm import Session, declarative_base
from datetime import datetime, date


DB_PATH = "./plants_orphange.db"
engine = create_engine(f"sqlite:///{DB_PATH}")
Base = declarative_base()

class Plants(Base):
    __tablename__ = "plants"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    type = Column(String)
    location = Column(String)
    water_every_days = Column(Integer)
    adopted_by = Column(String, nullable=True)


class Watering(Base):
    __tablename__ = "waterings"
    id = Column(Integer, primary_key=True)
    plant_id = Column(Integer, ForeignKey("plants.id"))
    roll_no = Column(String)
    watered_on = Column(DateTime , default=datetime.now())

Base.metadata.create_all(engine)


def get_all_plants(plant_type=None): #gives all plants, may be filtered with type
    session = Session(engine)
    if plant_type is None:
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
    else:
        plants = session.query(Plants).filter(Plants.type == plant_type)
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

def get_plant(id): #gets info about specific plant from id and gives all waterings
    session = Session(engine)
    plant = session.get(Plants, id)
    if not plant:
        session.close()
        return {"code":404,"msg":"Plant doesn't exist"}
    last_watered = session.query(Watering).filter(Plants.id == plant.id).order_by(Watering.plant_id.desc()).all()
    response = {
        "id": plant.id,
        "name": plant.name,
        "type": plant.type,
        "location": plant.location,
        "water_every_days": plant.water_every_days,
        "adopted_by": plant.adopted_by,
        "last_watered":last_watered
    }
    session.close()
    return {"plant":response,"code":200}

def add_plant(name,type,location,water_every_days):#adds new plants to database, E3
    session = Session(engine)
    plant = Plants(name=name, type=type,location=location,water_every_days=water_every_days,adopted_by= None)
    session.add(plant)
    response = {
        "id": plant.id,
        "name": plant.name,
        "type": plant.type,
        "location": plant.location,
        "water_every_days": plant.water_every_days,
        "adopted_by": plant.adopted_by,
    }
    session.commit()
    session.close()
    return response



def adopt_plant(plant_id , roll_no):
    session = Session(engine)
    plant = session.get(Plants, plant_id)
    if not plant:
        session.close()
        return {"code":404,"msg":"Plant Doesnt Exist"}
    if plant.adopted_by:
        session.close()
        return {"code":409,"msg":"Plant is already adopted"}
    plant.adopted_by = roll_no
    response = {"code":200, "plant":plant_to_dict(plant)}
    session.commit()

    session.close()
    return response


def give_up_plant(plant_id):
    session = Session(engine)
    plant = session.get(Plants, plant_id)
    if not plant:
        session.close()
        return {"code": 404, "msg": "Plant Doesnt Exist"}
    if not plant.adopted_by:
        session.close()
        return {"code": 409, "msg": "Plant is not adopted"}

    plant.adopted_by = None
    response = {"code":200, "plant":plant_to_dict(plant)}

    session.commit()
    session.close()
    return response




def plant_to_dict(plant: Plants):
    return {
        "id": plant.id,
        "name": plant.name,
        "type": plant.type,
        "location": plant.location,
        "water_every_days": plant.water_every_days,
        "adopted_by": plant.adopted_by
    }

def water_plant(plant_id, roll_no):
    session = Session(engine)
    plant = session.get(Plants, plant_id)
    if not plant:
        session.close()
        return {"code": 404, "msg": "Plant Doesnt Exist"}

    if plant.adopted_by != roll_no:
        session.close()
        return {"code": 403, "msg": "Plant is not adopted by you"}
    last_watered = session.query(Watering).join(Plants).filter(Plants.id == plant_id).order_by(Watering.plant_id.desc()).one_or_none()

    if last_watered  and datetime.today().date() == last_watered.watered_on.date():
        session.close()
        return {"code": 409, "msg": "Plant has been already watered today"}
    new_watered = Watering(plant_id=plant_id,roll_no=roll_no)
    session.add(new_watered)
    response = {"code":200, "watering":plant_to_dict(plant)}
    session.commit()
    session.close()

    return response



def watering_to_dict(watering:Watering):
    return {
        "id":watering.id,
        "plant_id": watering.plant_id,
        "roll_no": watering.roll_no,
        "watered_on": watering.watered_on.date()
    }

def need_to_water_today(): #gets the plants that need to be watered today, E7
    session = Session(engine)
    plants = session.query(Plants).all()
    response = []
    for plant in plants:
        last_watered = session.query(Watering).filter(Plants.id == plant.id).order_by(Watering.plant_id.desc()).one_or_none()
        temp_plant = {
            "id": plant.id,
            "name": plant.name,
            "type": plant.type,
            "location": plant.location,
            "water_every_days": plant.water_every_days,
            "adopted_by": plant.adopted_by,
            "last_watered": last_watered
        }
        if last_watered and (datetime.today().date() - last_watered.watered_on.date()).days >= plant.water_every_days:
            response.append(temp_plant)
    session.close()
    return response