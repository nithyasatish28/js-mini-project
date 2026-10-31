from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import Session, declarative_base
from fastapi import FastAPI, HTTPException

DB_PATH = "umbrellas.db"
engine = create_engine(f"sqlite:///{DB_PATH}")
Base = declarative_base()

class stations(Base):
    __tablename__ = "Stations"
    station_id = Column(Integer, primary_key=True)
    name = Column(String)
    location = Column(String)
    capacity = Column(Integer)
    umbrellas_available = Column(Integer)

class borrows(Base):
    __tablename__ = "Borrows"
    id = Column(Integer, primary_key = True)
    roll_no = Column(String)
    from_station_id = Column(String, ForeignKey('Stations.station_id'))
    to_station_id = Column(String, ForeignKey('Stations.station_id'))
    borrowed_on = Column(DateTime, default=datetime.now)
    returned_on = Column(DateTime)

Base.metadata.create_all(engine)

def get_all_stations():
    session = Session(engine)
    Stations = session.query(stations).all()
    response = []
    for station in Stations:
        temp_station = {
            "id": station.station_id,
            "name": station.name,
            "location": station.location,
            "capacity": station.capacity,
            "umbrellas_available": station.umbrellas_available,
            "free_slots": station.capacity - station.umbrellas_available
        }

        response.append(temp_station)
    session.close()
    return response


def add_stations(name, location, capacity, umbrellas_available):
    session = Session(engine)
    Station = stations(name = name, location = location, capacity = capacity, umbrellas_available = umbrellas_available)
    session.add(Station)
    session.commit()
    
    response = {
        "station_id": Station.station_id,
        "name": Station.name,
        "location": Station.location,
        "capacity": Station.capacity,
        "umbrellas_available": Station.umbrellas_available
    }
    session.close()
    return response

def get_station_by_id(station_id):
    session = Session(engine)
    Station = session.get(stations, station_id)
    if Station is None:
        raise HTTPException (status_code = 404, detail = "Station_id not found")
    response = {
        "station_id": Station.station_id, # type: ignore
        "name": Station.name,
        "location": Station.location, # type: ignore
        "capacity": Station.capacity,
        "umbrellas_available": Station.umbrellas_available,
        "free_slots": Station.capacity - Station.umbrellas_available
    }
    session.close()
    return response


def get_active_borrow(roll_no):
    session = Session(engine)
    borrow_record = session.query(borrows).filter(borrows.roll_no == str(roll_no), borrows.returned_on == None).first()
    
    if borrow_record is None:
        session.close()
        return None
        
    response = {
        "id": borrow_record.id,
        "roll_no": borrow_record.roll_no,
        "from_station_id": borrow_record.from_station_id,
        "borrowed_on": borrow_record.borrowed_on
    }
    session.close()
    return response


def borrow_umbrella(roll_no, station_id):
    session = Session(engine)
    Station = session.get(stations, int(station_id))
    Station.umbrellas_available -= 1

    Borrow = borrows(roll_no=roll_no, from_station_id=int(station_id), borrowed_on=datetime.now())
    session.add(Borrow)
    session.commit()
    session.close()
    return {"message": "Umbrella borrowed successfully"}


def return_umbrella(roll_no, station_id):
    session = Session(engine)
    borrow_record = session.query(borrows).filter(borrows.roll_no == str(roll_no), borrows.returned_on == None).first()
    
    Station = session.get(stations, int(station_id))
    
    if not borrow_record or not Station:
        session.close()
        return {"error": "Dont have record for this borrow or station"}
        
    Station.umbrellas_available += 1
    borrow_record.to_station_id = int(station_id)
    borrow_record.returned_on = datetime.now()
    
    session.commit()
    session.close()
    return {"message": "Umbrella returned successfully"}



def get_student_borrow(roll_no):
    session = Session(engine)
    result = session.query(borrows, stations.name).join(stations, stations.station_id == borrows.from_station_id).filter(
        borrows.roll_no == str(roll_no),
        borrows.returned_on == None
    ).first()

    if result is None:
        session.close()
        return None
        
    borrow_rec, station_name = result
    response = {
        "id": borrow_rec.id,
        "roll_no": borrow_rec.roll_no,
        "from_station_id": borrow_rec.from_station_id,
        "from_station_name": station_name,
        "borrowed_on": borrow_rec.borrowed_on
    }
    session.close()
    return response


def get_attention_stations():

    session = Session(engine)
    Stations = session.query(stations).all()
    response = []

    for Station in Stations:

        free_slots = Station.capacity - Station.umbrellas_available

        if Station.umbrellas_available == 0 or free_slots == 0:

            temp_station = {
                "station_id": Station.station_id,
                "name": Station.name,
                "location": Station.location,
                "capacity": Station.capacity,
                "umbrellas_available": Station.umbrellas_available,
                "free_slots": free_slots
            }

            response.append(temp_station)

    session.close()

    return response


  









