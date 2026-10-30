from sqlalchemy import Integer, String, Column, Date, ForeignKey, create_engine
from sqlalchemy.orm import Session, declarative_base
from datetime import date, timedelta
from fastapi import HTTPException


DB_PATH = "garden.db"
engine = create_engine(f"sqlite:///{DB_PATH}")
Base = declarative_base()


class Plants(Base):
    __tablename__ = "plants"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    type = Column(String)
    location = Column(String)
    water_every_days = Column(Integer)
    adopted_by = Column(String, nullable=True)      # None = nobody has adopted it


class Waterings(Base):
    __tablename__ = "waterings"
    id = Column(Integer, primary_key=True)
    plant_id = Column(Integer, ForeignKey("plants.id"))
    roll_no = Column(String)
    watered_on = Column(Date)


Base.metadata.create_all(engine)


def seed():
    session = Session(engine)
    if session.query(Plants).count() == 0:          # only add plants if the table is empty
        plants = [
            Plants(name="Tulsi", type="herb", location="Block A garden", water_every_days=2, adopted_by="21CS001"),
            Plants(name="Aloe Vera", type="succulent", location="Library window", water_every_days=10, adopted_by="21CS002"),
            Plants(name="Rose", type="flowering", location="Main gate", water_every_days=2, adopted_by="21CS003"),
            Plants(name="Money Plant", type="indoor", location="Admin office", water_every_days=5, adopted_by="21CS001"),
            Plants(name="Neem", type="tree", location="Canteen", water_every_days=7, adopted_by="21CS004"),
            Plants(name="Mint", type="herb", location="Hostel terrace", water_every_days=1, adopted_by="21CS005"),
            Plants(name="Jade Plant", type="succulent", location="Lab 3", water_every_days=14),
            Plants(name="Hibiscus", type="flowering", location="Block B entrance", water_every_days=3),
            Plants(name="Snake Plant", type="indoor", location="Reception", water_every_days=10),
            Plants(name="Mango", type="tree", location="Sports ground", water_every_days=7),
        ]
        session.add_all(plants)
        session.commit()

        today = date.today()
        waterings = [
            Waterings(plant_id=1, roll_no="21CS001", watered_on=today - timedelta(days=5)),   # Tulsi: due
            Waterings(plant_id=2, roll_no="21CS002", watered_on=today - timedelta(days=1)),   # Aloe: not due
            Waterings(plant_id=3, roll_no="21CS003", watered_on=today - timedelta(days=6)),
            Waterings(plant_id=3, roll_no="21CS003", watered_on=today - timedelta(days=4)),   # Rose: due
            Waterings(plant_id=4, roll_no="21CS001", watered_on=today - timedelta(days=2)),   # Money Plant: not due
            Waterings(plant_id=5, roll_no="21CS004", watered_on=today - timedelta(days=2)),   # Neem: not due
            Waterings(plant_id=6, roll_no="21CS005", watered_on=today - timedelta(days=1)),   # Mint: due
        ]
        session.add_all(waterings)
        session.commit()
    session.close()


# E1: get all plants (can be filtered by type), each with its last watered date
def get_all_plants(type=None):
    session = Session(engine)
    if type is None:
        plants = session.query(Plants).all()                                 # select * from plants
    else:
        plants = session.query(Plants).filter(Plants.type == type).all()     # select * from plants where type = ?
    response = []
    for plant in plants:
        last = (session.query(Waterings)
                .filter(Waterings.plant_id == plant.id)
                .order_by(Waterings.watered_on.desc())
                .first())                                                    # newest watering, or None
        if last is None:
            last_watered = None
            needs_water = True                                               # never watered
        else:
            last_watered = str(last.watered_on)
            needs_water = (date.today() - last.watered_on).days >= plant.water_every_days

        temp_plant = {
            "id": plant.id,
            "name": plant.name,
            "type": plant.type,
            "location": plant.location,
            "water_every_days": plant.water_every_days,
            "adopted_by": plant.adopted_by,
            "last_watered": last_watered,
            "needs_water": needs_water
        }
        response.append(temp_plant)
    session.close()
    return response


# E2: get one plant by id, with its list of waterings, newest first
def get_plant(id):
    session = Session(engine)
    plant = session.get(Plants, id)
    if plant is None:
        session.close()
        raise HTTPException(status_code=404, detail="Plant not found.")

    waterings = (session.query(Waterings)
                 .filter(Waterings.plant_id == id)
                 .order_by(Waterings.watered_on.desc())
                 .all())                                                     # newest first
    if len(waterings) == 0:
        last_watered = None
        needs_water = True
    else:
        last_watered = str(waterings[0].watered_on)
        needs_water = (date.today() - waterings[0].watered_on).days >= plant.water_every_days

    watering_list = []
    for w in waterings:
        temp_watering = {
            "id": w.id,
            "roll_no": w.roll_no,
            "watered_on": str(w.watered_on)
        }
        watering_list.append(temp_watering)

    response = {
        "id": plant.id,
        "name": plant.name,
        "type": plant.type,
        "location": plant.location,
        "water_every_days": plant.water_every_days,
        "adopted_by": plant.adopted_by,
        "last_watered": last_watered,
        "needs_water": needs_water,
        "waterings": watering_list
    }
    session.close()
    return response


# E3: add a new plant. Nobody has adopted it yet.
def add_plant(name, type, location, water_every_days):
    session = Session(engine)
    plant = Plants(name=name, type=type, location=location,
                   water_every_days=water_every_days, adopted_by=None)
    session.add(plant)
    session.commit()                  # commit FIRST, so the plant gets its id
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


# E4: adopt a plant with a roll number
def adopt_plant(id, roll_no):
    session = Session(engine)
    plant = session.get(Plants, id)
    if plant is None:
        session.close()
        raise HTTPException(status_code=404, detail="Plant not found.")

    if plant.adopted_by is not None:
        session.close()
        raise HTTPException(status_code=409, detail="This plant has already been adopted.")

    count = session.query(Plants).filter(Plants.adopted_by == roll_no).count()
    if count >= 2:
        session.close()
        raise HTTPException(status_code=409, detail="You have already adopted 2 plants.")

    plant.adopted_by = roll_no
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


# E5: give up (un-adopt) a plant
def unadopt_plant(id):
    session = Session(engine)
    plant = session.get(Plants, id)
    if plant is None:
        session.close()
        raise HTTPException(status_code=404, detail="Plant not found.")

    if plant.adopted_by is None:
        session.close()
        raise HTTPException(status_code=409, detail="Nobody has adopted this plant.")

    plant.adopted_by = None
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


# E6: log a watering with a roll number. The date is today.
def water_plant(id, roll_no):
    session = Session(engine)
    plant = session.get(Plants, id)
    if plant is None:
        session.close()
        raise HTTPException(status_code=404, detail="Plant not found.")

    if plant.adopted_by != roll_no:
        session.close()
        raise HTTPException(status_code=403, detail="Only the student who adopted this plant can water it.")

    already = (session.query(Waterings)
               .filter(Waterings.plant_id == id, Waterings.watered_on == date.today())
               .first())
    if already is not None:
        session.close()
        raise HTTPException(status_code=409, detail="This plant has already been watered today.")

    watering = Waterings(plant_id=id, roll_no=roll_no, watered_on=date.today())
    session.add(watering)
    session.commit()
    response = {
        "id": watering.id,
        "plant_id": watering.plant_id,
        "roll_no": watering.roll_no,
        "watered_on": str(watering.watered_on)
    }
    session.close()
    return response


# E7: get the plants that need water today
def get_needs_water():
    all_plants = get_all_plants()             # E1 already works out needs_water for each plant
    response = []
    for plant in all_plants:
        if plant["needs_water"] == True:
            response.append(plant)
    return response
