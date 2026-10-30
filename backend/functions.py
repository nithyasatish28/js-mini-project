from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import Session, declarative_base

DB_PATH = "umbrellas.db"
engine = create_engine(f"sqlite:///{DB_PATH}")
Base = declarative_base()

class stations(Base):
    __tablename__ = "Stations"
    station_id = Column(String, primary_key=True)
    name = Column(String)
    location = Column(String)
    capacity = Column(Integer)
    umbrellas_available = Column(Integer)

class borrows(Base):
    __tablename__ = "Borrows"
    roll_no = Column(String, primary_key=True)
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
            "umbrellas_available": station.umbrellas_available
        }

        response.append(temp_station)
    session.close()
    return response


# def add_stations(station_id, name, location, capacity, umbrellas_available):
#     session = Session(engine)
#     Station = stations(station_id = station_id, name = name, location = location, capacity = 20, umbrellas_available = umbrellas_available)
#     session.add(Station)
#     response = {
#         "station_id": Station.station_id,
#         "name": Station.name,
#         "location": Station.location,
#         "capacity": Station.capacity,
#         "umbrellas_available": Station.umbrellas_available
#     }
#     session.commit()
#     session.close()
#     return response

def get_station_by_id(station_id):
    session = Session(engine)
    Station = session.get(stations, station_id)
    response = {
        "station_id": Station.station_id,
        "name": Station.name,
        "location": Station.location,
        "capacity": Station.capacity,
        "umbrellas_available": Station.umbrellas_available,
    }
    session.close()
    return response

def update_stations(station_id, name, location, capacity, umbrellas_available):
    session = Session(engine)
    Station = stations(station_id = station_id, name = name, location = location, capacity = 20, umbrellas_available = umbrellas_available)
    session.add(Station)
    response = {
        "station_id": Station.station_id,
        "name": Station.name,
        "location": Station.location,
        "capacity": Station.capacity,
        "umbrellas_available": Station.umbrellas_available
    }
    session.commit()
    session.close()
    return response










