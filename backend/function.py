from sqlalchemy import Integer, String, Column, create_engine, DateTime, ForeignKey
from sqlalchemy.orm import Session, declarative_base
from datetime import datetime

DB_PATH = "umbrellas.db"

engine = create_engine(f"sqlite:///{DB_PATH}")
Base = declarative_base()


class Stations(Base):
    __tablename__ = "stations"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    capacity = Column(Integer, nullable=False)
    umbrellas_available = Column(Integer, nullable=False)


class Borrows(Base):
    __tablename__ = "borrows"

    id = Column(Integer, primary_key=True)
    roll_no = Column(String, nullable=False)
    from_station_id = Column(Integer, ForeignKey("stations.id"))
    to_station_id = Column(Integer, ForeignKey("stations.id"), nullable=True)
    borrowed_on = Column(DateTime, default=datetime.now)
    returned_on = Column(DateTime, nullable=True)


Base.metadata.create_all(engine)

def add_initial_stations():
    session = Session(engine)

    count = session.query(Stations).count()

    if count == 0:
        stations = [
            Stations(name="Main Gate", location="Main Entrance", capacity=10, umbrellas_available=10),
            Stations(name="Library", location="Central Library", capacity=10, umbrellas_available=5),
            Stations(name="Canteen", location="College Canteen", capacity=10, umbrellas_available=0),
            Stations(name="Academic Block", location="Academic Building", capacity=10, umbrellas_available=7),
            Stations(name="Hostel", location="Hostel Entrance", capacity=10, umbrellas_available=3)
        ]

        session.add_all(stations)
        session.commit()

    session.close()
def get_all_stations():
    session = Session(engine)

    stations = session.query(Stations).all()

    result = []

    for station in stations:
        result.append({
            "id": station.id,
            "name": station.name,
            "location": station.location,
            "capacity": station.capacity,
            "umbrellas_available": station.umbrellas_available,
            "free_slots": station.capacity - station.umbrellas_available
        })

    session.close()
    return result

def get_station(station_id):
    session = Session(engine)

    station = session.query(Stations).filter(Stations.id == station_id).first()

    if station is None:
        session.close()
        return None

    result = {
        "id": station.id,
        "name": station.name,
        "location": station.location,
        "capacity": station.capacity,
        "umbrellas_available": station.umbrellas_available,
        "free_slots": station.capacity - station.umbrellas_available
    }

    session.close()
    return result