from sqlalchemy import String,Column,Integer,create_engine,DateTime
from sqlalchemy.orm import Session ,declarative_base
from datetime import datetime

DB_PATH = "umbrellas.db"
engine = create_engine(f"sqlite:///{DB_PATH}")
Base = declarative_base()

class Stations(Base):
    __tablename__ ="stations"
    id =Column(Integer , primary_key =True)
    name = Column(String)
    location = Column(String)
    capacity = Column(Integer)
    umbrellas_available = Column(Integer)


class Borrows(Base):
      __tablename__ = "borrows"
      borrow_id =Column(Integer, primary_key =True)
      roll_no = Column(Integer )
      from_station_id = Column(Integer)
      to_station_id =Column(Integer)
      borrowed_on = Column(DateTime, nullable=True) 
      returned_on = Column(DateTime, nullable=True) 

Base.metadata.create_all(engine)


def get_all_stations():
    session = Session(engine)
    stations = session.query(Stations).all()
    response = []
    for station in stations:
        temp_station ={
            "id":station.id,
            "name":station.name,
            "location":station.location,
            "capacity":station.capacity,
            "umbrellas_available": station.umbrellas_available,
        }
        response.append(temp_station)
    session.close()
    return response

def add_stations(name, capacity, umbrellas_available, location = None):
    session = Session(engine)
    station = Stations( name=name, capacity=capacity, umbrellas_available = umbrellas_available, location=location) 
    session.add(station)
    session.commit() 
    response = {
        "id":station.id,
        "name":station.name,
        "location":station.location,
        "capacity":station.capacity,
        "umbrellas_available": station.umbrellas_available,

    }
    session.close()
    return response


def get_station_by_id(id):
    session = Session(engine)
    station = session.get(Stations, id) 
    if station is None:
        session.close()
        return None
    response = {
        "id": station.id,
        "name": station.name,
        "umbrellas_available": station.umbrellas_available,
        "capacity": station.capacity,
        "location": station.location,
        
    }
    session.close()
    return response


def borrow_umbrella_station(roll_no,id ):
    session = Session(engine)
    station =session.get(Stations,int(id))
    if not station:
        session.close()
        return {"error": "station not found"}
    
    station.umbrellas_available-=1

    Borrow = Borrows(roll_no=roll_no ,from_station_id=int(id),borrowed_on=datetime.now())
    session.add(Borrow)
    session.commit()
    session.close()
    return {"message" : "umbrella borrowed successfully"}

def return_umbrella_station(roll_no,id,returned_on=None):
    session = Session(engine)
    borrow_record = session.query(Borrows).filter(
        Borrows.roll_no == str(roll_no),
        Borrows.returned_on == None
    ).first()
    station =session.get(Stations, int(id))

    if not borrow_record or not station:
        session.close()
        return {"error" : "Data matching failed : no record found"}

    station.umbrellas_available +=1
    borrow_record.to_station_id = int(id)
    borrow_record.returned_on = datetime.now()
    
    session.commit()
    session.close()
    return {"message" : "umbrellas returned succussfully"}

def get_unreturned_umbrella_by_roll(roll_no):
    session = Session(engine)
    result = session.query(Borrows, Stations.name).join(
        Stations, Stations.id == Borrows.from_station_id
    ).filter(
            Borrows.roll_no == str(roll_no),
            Borrows.returned_on == None  
    ).first()

    if result is None:
        session.close()
        return None
    
    borrow_record, station_name= result
    response = {
        "borrow_id": borrow_record.borrow_id,
        "roll_no": borrow_record.roll_no,
        "from_station_id": borrow_record.from_station_id,
        "from_station_name": station_name,  
        "borrowed_on": borrow_record.borrowed_on
        }
        
    session.close()
    return response


def get_stations_need_attention():
    session = Session(engine)
    stations = session.query(Stations).all()
    response =[]

    for station in stations:
        free_slots = station.capacity - station.umbrellas_available

        if station.umbrellas_available == 0 or free_slots==0:

           temp_station = {
                   "id":station.id,
                   "name":station.name,
                   "location":station.location,
                   "capacity":station.capacity,
                   "umbrellas_available": station.umbrellas_available ,
                   "free_slots": free_slots 
           }

           response.append(temp_station)

    session.close()
    return response
