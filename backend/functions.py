from sqlalchemy import Integer, String, Column, ForeignKey, create_engine, DateTime
from sqlalchemy.orm import Session, declarative_base
from datetime import datetime

DB_PATH = "backend/umbrellas.db"
engine = create_engine(f"sqlite:///{DB_PATH}")
Base = declarative_base()

class Stations(Base):
    __tablename__ = "stations"

    id = Column[int](Integer, primary_key=True)
    name = Column[str](String,nullable=False)
    location = Column[str](String, nullable=False)
    capacity = Column[int](Integer,nullable=False)
    umbrellas_available = Column[int](Integer,nullable=False)

class Borrows(Base):
    __tablename__ = "borrows"

    id = Column[int](Integer, primary_key=True)
    roll_no = Column[str](String, nullable=False)
    from_station_id = Column[int](Integer, ForeignKey("stations.id"), nullable=False)
    to_station_id = Column[int](Integer, ForeignKey("stations.id"), nullable=True)
    borrowed_on = Column[DateTime](DateTime, default=datetime.now)
    returned_on = Column[DateTime](DateTime, nullable = True)

Base.metadata.create_all(engine)


def add_initial_stations():
    session = Session(engine)

    existing_station = session.query(Stations).first()

    if existing_station is None:
        stations = [
            Stations(name="Main Gate", location="Main Entrance", capacity=10, umbrellas_available=10),
            Stations(name="Library", location="Central Library", capacity=8, umbrellas_available=0),
            Stations(name="Cafeteria", location="Food Court", capacity=12, umbrellas_available=12),
            Stations(name="Sports Complex", location="Sports Ground", capacity=15, umbrellas_available=7),
            Stations(name="Admin Block", location="Office Area", capacity=6, umbrellas_available=3)
        ]

        session.add_all(stations)
        session.commit()

    session.close()

add_initial_stations()

def get_all_stations():
    session = Session(engine)

    stations = session.query(Stations).all()
    response = []

    for station in stations:
        temp_station = {
            "id": station.id,
            "name": station.name,
            "location": station.location,
            "capacity": station.capacity,
            "umbrellas_available": station.umbrellas_available,
            "free_slots": station.capacity - station.umbrellas_available
        }

        response.append(temp_station)

    session.close()
    return response

def get_station_by_id(station_id):
    session = Session(engine)

    station = session.query(Stations).filter(Stations.id == station_id).first()

    if station is None:
        session.close()
        return None

    response = {
        "id": station.id,
        "name": station.name,
        "location": station.location,
        "capacity": station.capacity,
        "umbrellas_available": station.umbrellas_available,
        "free_slots": station.capacity - station.umbrellas_available
    }

    session.close()
    return response

def add_station(name, location, capacity, umbrellas_available):
    session = Session(engine)

    station = Stations(
        name=name,
        location=location,
        capacity=capacity,
        umbrellas_available=umbrellas_available
    )

    session.add(station)
    session.commit()

    response = {
        "id": station.id,
        "name": station.name,
        "location": station.location,
        "capacity": station.capacity,
        "umbrellas_available": station.umbrellas_available,
        "free_slots": station.capacity - station.umbrellas_available
    }

    session.close()
    return response

def borrow_umbrella(roll_no, station_id):
    session = Session(engine)

    station = session.query(Stations).filter(Stations.id == station_id).first()

    if station is None:
        session.close()
        return None

    existing_borrow = session.query(Borrows).filter(Borrows.roll_no == roll_no, Borrows.returned_on == None).first()

    if existing_borrow:
        session.close()
        return "already_borrowed"

    if station.umbrellas_available == 0:
        session.close()
        return "no_umbrellas"

    station.umbrellas_available = station.umbrellas_available - 1

    borrow = Borrows(roll_no=roll_no, from_station_id=station_id)

    session.add(borrow)
    session.commit()

    response = {
        "id": borrow.id,
        "roll_no": borrow.roll_no,
        "from_station_id": borrow.from_station_id,
        "borrowed_on": borrow.borrowed_on
    }

    session.close()
    return response


def return_umbrella(borrow_id, station_id):
    session = Session(engine)

    borrow = session.query(Borrows).filter(Borrows.id == borrow_id).first()

    if borrow is None:
        session.close()
        return "borrow_not_found"

    if borrow.returned_on is not None:
        session.close()
        return "already_returned"

    station = session.query(Stations).filter(Stations.id == station_id).first()

    if station is None:
        session.close()
        return "station_not_found"

    if station.umbrellas_available == station.capacity:
        session.close()
        return "station_full"

    station.umbrellas_available = station.umbrellas_available + 1
    borrow.to_station_id = station_id
    borrow.returned_on = datetime.now()

    session.commit()

    response = {
        "id": borrow.id,
        "roll_no": borrow.roll_no,
        "from_station_id": borrow.from_station_id,
        "to_station_id": borrow.to_station_id,
        "borrowed_on": borrow.borrowed_on,
        "returned_on": borrow.returned_on
    }

    session.close()
    return response

def get_student_umbrella(roll_no):
    session = Session(engine)

    borrow = session.query(Borrows).filter(Borrows.roll_no == roll_no, Borrows.returned_on == None).first()

    if borrow is None:
        session.close()
        return None

    station = session.query(Stations).filter(Stations.id == borrow.from_station_id).first()

    response = {
        "borrow_id": borrow.id,
        "roll_no": borrow.roll_no,
        "from_station_id": borrow.from_station_id,
        "station_name": station.name,
        "borrowed_on": borrow.borrowed_on
    }

    session.close()
    return response

def get_stations_needs_attention():
    session = Session(engine)

    stations = session.query(Stations).all()
    response = []

    for station in stations:
        if station.umbrellas_available == 0 or station.umbrellas_available == station.capacity:

            temp_station = {
                "id": station.id,
                "name": station.name,
                "location": station.location,
                "capacity": station.capacity,
                "umbrellas_available": station.umbrellas_available,
                "free_slots": station.capacity - station.umbrellas_available
            }

            response.append(temp_station)

    session.close()
    return response

