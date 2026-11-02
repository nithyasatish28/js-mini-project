from sqlalchemy import Integer, String, Column, create_engine, DateTime, ForeignKey
from sqlalchemy.orm import Session, declarative_base
from datetime import datetime

DB_PATH = "umbrellas.db"

engine = create_engine(f"sqlite:///{DB_PATH}")
Base = declarative_base()

class Students(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    roll_no = Column(String, unique=True)
    name = Column(String)
    contact = Column(String)

class Stations(Base):
    __tablename__ = "stations"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    location = Column(String)
    capacity = Column(Integer)
    umbrellas_available = Column(Integer)

class Borrows(Base):
    __tablename__ = "borrows"

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    from_station_id = Column(Integer, ForeignKey("stations.id"))
    to_station_id = Column(Integer, ForeignKey("stations.id"), nullable=True)
    borrowed_on = Column(DateTime, default=datetime.now)
    returned_on = Column(DateTime, nullable=True)

Base.metadata.create_all(engine)

def add_initial_stations():

    session = Session(engine)

    stations = [
        Stations(name="library", location="3rd floor", capacity=10, umbrellas_available=10),
        Stations(name="canteen", location="basement", capacity=8, umbrellas_available=0),
        Stations(name="play ground", location="ground floor", capacity=12, umbrellas_available=6),
        Stations(name="lab", location="1st floor", capacity=15, umbrellas_available=9),
        Stations(name="main gate", location="entrance", capacity=6, umbrellas_available=3)
    ]

    for station in stations:

        old_station = session.query(Stations).filter(Stations.name == station.name).first()

        if old_station is None:
            session.add(station)

    session.commit()
    session.close()

add_initial_stations()
def add_student(roll_no, name, contact):

    session = Session(engine)

    old_student = session.query(Students).filter(Students.roll_no == roll_no).first()

    if old_student:
        session.close()
        return {"message": "Student already exists"}

    student = Students(roll_no=roll_no, name=name, contact=contact)

    session.add(student)
    session.commit()

    response = {
        "id": student.id,
        "roll_no": student.roll_no,
        "name": student.name,
        "contact": student.contact
    }

    session.close()
    return response

def get_all_stations():

    session = Session(engine)
    stations = session.query(Stations).all()
    response = []

    for station in stations:

        temp_station = {
            "id": station.id,
            "name": station.name,
            "location": station.location,
            "umbrellas_available": station.umbrellas_available,
            "free_slots": station.capacity - station.umbrellas_available
        }

        response.append(temp_station)

    session.close()
    return response

def get_station(id):

    session = Session(engine)

    station = session.query(Stations).filter(Stations.id == id).first()

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

    station = Stations(name=name,location=location,capacity=capacity,umbrellas_available=umbrellas_available)

    session.add(station)
    session.commit()

    response = {
        "id": station.id,
        "name": station.name,
        "location": station.location,
        "capacity": station.capacity,
        "umbrellas_available": station.umbrellas_available
    }

    session.close()
    return response

def borrow_umbrella(roll_no, station_id):

    session = Session(engine)

    student = session.query(Students).filter(Students.roll_no == roll_no).first()

    station = session.query(Stations).filter(Stations.id == station_id).first()

    if student is None:
        session.close()
        return {"message": "Student not found"}

    if station is None:
        session.close()
        return {"message": "Station not found"}

    if station.umbrellas_available == 0:
        session.close()
        return {"message": "No umbrellas available"}

    old_borrow = session.query(Borrows).filter(Borrows.student_id == student.id,Borrows.returned_on == None).first()

    if old_borrow:
        session.close()
        return {"message": "Already borrowed"}

    borrow = Borrows(
        student_id=student.id,
        from_station_id=station_id,
        borrowed_on=datetime.now()
    )

    station.umbrellas_available = station.umbrellas_available - 1

    session.add(borrow)
    session.commit()
    session.close()

    return {"message": "Umbrella borrowed successfully"}

def return_umbrella(roll_no, station_id):

    session = Session(engine)

    student = session.query(Students).filter(Students.roll_no == roll_no).first()

    if student is None:
        session.close()
        return {"message": "Student not found"}

    borrow = session.query(Borrows).filter(Borrows.student_id == student.id,Borrows.returned_on == None).first()

    if borrow is None:
        session.close()
        return {"message": "No umbrella borrowed"}

    station = session.query(Stations).filter(Stations.id == station_id).first()

    if station is None:
        session.close()
        return {"message": "Station not found"}

    if station.umbrellas_available >= station.capacity:
        session.close()
        return {"message": "Station is full"}

    station.umbrellas_available = station.umbrellas_available + 1

    borrow.to_station_id = station_id
    borrow.returned_on = datetime.now()

    session.commit()
    session.close()

    return {"message": "Umbrella returned successfully"}

def get_student_borrow(roll_no):

    session = Session(engine)

    student = session.query(Students).filter(Students.roll_no == roll_no).first()

    if student is None:
        session.close()
        return {"message": "Student not found"}

    borrow = session.query(Borrows).filter(Borrows.student_id == student.id,Borrows.returned_on == None).first()

    if borrow:

        station = session.query(Stations).filter(Stations.id == borrow.from_station_id).first()

        response = {
            "roll_no": student.roll_no,
            "name": student.name,
            "station_name": station.name if station else None,
            "borrowed_on": borrow.borrowed_on
        }

        session.close()
        return response

    session.close()
    return {"message": "No unreturned umbrella found"}

def get_attention_stations():

    session = Session(engine)

    stations = session.query(Stations).all()
    response = []

    for station in stations:

        free_slots = station.capacity - station.umbrellas_available

        if station.umbrellas_available == 0 or free_slots == 0:

            temp_station = {
                "id": station.id,
                "name": station.name,
                "location": station.location,
                "umbrellas_available": station.umbrellas_available,
                "free_slots": free_slots
            }

            response.append(temp_station)

    session.close()
    return response