from sqlalchemy import Integer, String, Column, create_engine, DateTime, ForeignKey
from sqlalchemy.orm import Session, declarative_base
from datetime import datetime
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "umbrellas.db")

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

    station = session.query(Stations).filter(
        Stations.id == station_id
    ).first()

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
    session.refresh(station)

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


def borrow_umbrella(roll_no, from_station_id):
    session = Session(engine)

    station = session.query(Stations).filter(
        Stations.id == from_station_id
    ).first()

    if station is None:
        session.close()
        return {"error": "Station not found", "status_code": 404}

    active_borrow = session.query(Borrows).filter(
        Borrows.roll_no == roll_no,
        Borrows.returned_on.is_(None)
    ).first()

    if active_borrow:
        session.close()
        return {
            "error": "Student already has an active borrow",
            "status_code": 400
        }

    if station.umbrellas_available == 0:
        session.close()
        return {
            "error": "No umbrellas available at this station",
            "status_code": 400
        }

    station.umbrellas_available -= 1

    borrow = Borrows(
        roll_no=roll_no,
        from_station_id=from_station_id,
        borrowed_on=datetime.now()
    )

    session.add(borrow)
    session.commit()
    session.refresh(borrow)

    result = {
        "message": "Umbrella borrowed successfully",
        "borrow_id": borrow.id,
        "roll_no": borrow.roll_no,
        "from_station_id": borrow.from_station_id,
        "borrowed_on": borrow.borrowed_on
    }

    session.close()
    return result


def return_umbrella(borrow_id, to_station_id):
    session = Session(engine)

    borrow = session.query(Borrows).filter(
        Borrows.id == borrow_id
    ).first()

    if borrow is None:
        session.close()
        return {
            "error": "Borrow record not found",
            "status_code": 404
        }

    if borrow.returned_on is not None:
        session.close()
        return {
            "error": "Umbrella has already been returned",
            "status_code": 400
        }

    station = session.query(Stations).filter(
        Stations.id == to_station_id
    ).first()

    if station is None:
        session.close()
        return {"error": "Station not found", "status_code": 404}

    if station.umbrellas_available >= station.capacity:
        session.close()
        return {"error": "Station is full", "status_code": 400}

    station.umbrellas_available += 1
    borrow.to_station_id = to_station_id
    borrow.returned_on = datetime.now()

    session.commit()

    result = {
        "message": "Umbrella returned successfully",
        "borrow_id": borrow.id,
        "roll_no": borrow.roll_no,
        "to_station_id": borrow.to_station_id,
        "returned_on": borrow.returned_on
    }

    session.close()
    return result


def get_active_borrow(roll_no):
    session = Session(engine)

    borrow = session.query(Borrows, Stations.name).join(
        Stations,
        Borrows.from_station_id == Stations.id
    ).filter(
        Borrows.roll_no == roll_no,
        Borrows.returned_on.is_(None)
    ).first()

    if borrow is None:
        session.close()
        return None

    borrow_data = borrow[0]
    station_name = borrow[1]

    result = {
        "borrow_id": borrow_data.id,
        "roll_no": borrow_data.roll_no,
        "from_station_id": borrow_data.from_station_id,
        "station_name": station_name,
        "borrowed_on": borrow_data.borrowed_on
    }

    session.close()
    return result


def get_all_active_borrows():
    session = Session(engine)

    borrows = session.query(Borrows, Stations.name).join(
        Stations,
        Borrows.from_station_id == Stations.id
    ).filter(
        Borrows.returned_on.is_(None)
    ).order_by(Borrows.borrowed_on.desc()).all()

    result = []

    for borrow_data, station_name in borrows:
        result.append({
            "borrow_id": borrow_data.id,
            "roll_no": borrow_data.roll_no,
            "from_station_id": borrow_data.from_station_id,
            "station_name": station_name,
            "borrowed_on": borrow_data.borrowed_on
        })

    session.close()
    return result


def get_attention_stations():
    session = Session(engine)

    stations = session.query(Stations).filter(
        (Stations.umbrellas_available == 0) |
        (Stations.umbrellas_available == Stations.capacity)
    ).all()

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