from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


DB_PATH = "umbrellas.db"

engine = create_engine(f"sqlite:///{DB_PATH}")
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# STATIONS TABLE

class Stations(Base):
    __tablename__ = "stations"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    capacity = Column(Integer, nullable=False)
    umbrellas_available = Column(Integer, nullable=False)

# BORROWS TABLE


class Borrows(Base):
    __tablename__ = "borrows"

    id = Column(Integer, primary_key=True)
    roll_no = Column(String, nullable=False)
    from_station_id = Column(Integer, ForeignKey("stations.id"), nullable=False)
    to_station_id = Column(Integer, ForeignKey("stations.id"), nullable=True)
    borrowed_on = Column(DateTime, default=datetime.utcnow)
    returned_on = Column(DateTime, nullable=True)

Base.metadata.create_all(engine)

# STATION RESPONSE


def _station_response(station):
    return {
        "id": station.id,
        "name": station.name,
        "location": station.location,
        "capacity": station.capacity,
        "umbrellas_available": station.umbrellas_available,
        "free_slots": station.capacity - station.umbrellas_available
    }

# BORROW RESPONSE


def _borrow_response(borrow):
    return {
        "id": borrow.id,
        "roll_no": borrow.roll_no,
        "from_station_id": borrow.from_station_id,
        "to_station_id": borrow.to_station_id,
        "borrowed_on": borrow.borrowed_on,
        "returned_on": borrow.returned_on
    }

#1

def get_all_stations():
    with SessionLocal() as db:
        stations = db.query(Stations).all()
        return [_station_response(station) for station in stations]

#2 get one station

def get_station(id):
    with SessionLocal() as db:
        station = db.get(Stations, id)
        return _station_response(station) if station is not None else None


#E3 - ADD STATION

def add_station(name, location, capacity, umbrellas_available):

    if not name or not name.strip():
        return {"error": "Station name is required.", "status_code": 422}

    if not location or not location.strip():
        return {"error": "Station location is required.", "status_code": 422}

    if type(capacity) is not int or capacity < 1 or capacity > 30:
        return {"error": "Capacity must be between 1 and 30.", "status_code": 422}

    if type(umbrellas_available) is not int or umbrellas_available < 0 or umbrellas_available > capacity:
        return {"error": "Starting umbrellas must be between 0 and capacity.", "status_code": 422}

    with SessionLocal() as db:
        station = Stations(
            name=name.strip(),
            location=location.strip(),
            capacity=capacity,
            umbrellas_available=umbrellas_available
        )

        db.add(station)
        db.commit()
        db.refresh(station)

        return _station_response(station)

#4borrow umbrella

def borrow_umbrella(station_id, roll_no):

    if not roll_no or not roll_no.strip():
        return {"error": "Roll number is required.", "status_code": 422}

    with SessionLocal() as db:

        station = db.get(Stations, station_id)

        if station is None:
            return {"error": "Station not found.", "status_code": 404}

        active_borrow = db.query(Borrows).filter(
            Borrows.roll_no == roll_no.strip(),
            Borrows.returned_on == None
        ).first()

        if active_borrow is not None:
            return {
                "error": "Student already has an unreturned umbrella.",
                "status_code": 409
            }

        if station.umbrellas_available == 0:
            return {
                "error": "This station is empty. Try another one.",
                "status_code": 409
            }

        station.umbrellas_available -= 1

        borrow = Borrows(
            roll_no=roll_no.strip(),
            from_station_id=station_id,
            borrowed_on=datetime.utcnow()
        )

        db.add(borrow)
        db.commit()
        db.refresh(borrow)

        return _borrow_response(borrow)


#5return umbrella

def return_umbrella(borrow_id, to_station_id):

    with SessionLocal() as db:

        borrow = db.get(Borrows, borrow_id)

        if borrow is None:
            return {"error": "Borrow record not found.", "status_code": 404}

        if borrow.returned_on is not None:
            return {
                "error": "This umbrella has already been returned.",
                "status_code": 409
            }

        station = db.get(Stations, to_station_id)

        if station is None:
            return {
                "error": "Destination station not found.",
                "status_code": 404
            }

        if station.umbrellas_available >= station.capacity:
            return {
                "error": "This station is full. Try another one.",
                "status_code": 409
            }

        station.umbrellas_available += 1

        borrow.to_station_id = to_station_id
        borrow.returned_on = datetime.utcnow()

        db.commit()
        db.refresh(borrow)

        return _borrow_response(borrow)

# get student's active borrow

def get_active_borrow(roll_no):

    with SessionLocal() as db:

        result = db.query(Borrows,Stations.name).join(Stations,Stations.id == Borrows.from_station_id
        ).filter(Borrows.roll_no == roll_no,Borrows.returned_on == None
        ).first()
        if result is None:
            return None
        borrow, station_name = result

        return {"borrow_id": borrow.id,
            "roll_no": borrow.roll_no,
            "from_station_id": borrow.from_station_id,
            "from_station_name": station_name,
            "borrowed_on": borrow.borrowed_on
        }


# get empty and full stations

def get_stations_needing_attention():

    with SessionLocal() as db:

        stations = db.query(Stations).filter(
            (Stations.umbrellas_available == 0) |
            (Stations.umbrellas_available == Stations.capacity)
        ).all()

        return [_station_response(station) for station in stations]