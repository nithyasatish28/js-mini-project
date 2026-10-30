from sqlalchemy import Integer, String, Column, create_engine
from sqlalchemy.orm  import Session, declarative_base
from datetime import datetime
from fastapi import HTTPException 

DB_PATH = "lab.db"
engine = create_engine(f"sqlite:///{DB_PATH}")
Base = declarative_base()

VALID_TYPES = ["microscope", "oscilloscope", "3d-printer", "laptop", "camera"]


class Equipment(Base):
    __tablename__ = "equipment"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    type = Column(String)
    lab_room = Column(String)
    in_service = Column(Integer, default=1)


class Bookings(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True)
    equipment_id = Column(Integer)
    roll_no = Column(String)
    booking_date = Column(String)
    booked_on = Column(String)
    cancelled = Column(Integer, default=0)


Base.metadata.create_all(engine)

def equipment_to_dict(item):
    return {
        "id": item.id,
        "name": item.name,
        "type": item.type,
        "lab_room": item.lab_room,
        "in_service": item.in_service
    }

def add_starting_items():
    session = Session(engine)
    count = session.query(Equipment).count()
    if count == 0:
        items = [
            Equipment(name="Glitter Microscope ", type="microscope", lab_room="Lab 101", in_service=1),
            Equipment(name="Barbie Microscope ", type="microscope", lab_room="Lab 101", in_service=1),
            Equipment(name="Pink Oscilloscope ", type="oscilloscope", lab_room="Lab 202", in_service=1),
            Equipment(name="Blue Oscilloscope ", type="oscilloscope", lab_room="Lab 202", in_service=0),
            Equipment(name="Magical 3D Printer", type="3d-printer", lab_room="Lab 305", in_service=1),
            Equipment(name="Galaxy 3D Printer", type="3d-printer", lab_room="Lab 305", in_service=1),
            Equipment(name="Apple Laptop 1", type="laptop", lab_room="Lab 110", in_service=1),
            Equipment(name="Apple Laptop 2", type="laptop", lab_room="Lab 110", in_service=1),
            Equipment(name="Canon DSLR", type="camera", lab_room="Media Room", in_service=1),
            Equipment(name="GoPro Hero", type="camera", lab_room="Media Room", in_service=1),
        ]
        session.add_all(items)
        session.commit()
    session.close()


add_starting_items()


