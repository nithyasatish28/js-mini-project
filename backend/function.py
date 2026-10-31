from datetime import datetime, date

from sqlalchemy import (Column,Date,DateTime,ForeignKey,Integer,String,create_engine,)
from sqlalchemy.orm import declarative_base, sessionmaker

session_PATH = "lab.session"

engine = create_engine(f"sqlite:///{session_PATH}")
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

VALID_TYPES = ["microscope","oscilloscope","3d-printer","laptop","camera"]

class Equipment(Base):
    __tablename__ = "equipment"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    lab_room = Column(String, nullable=False)
    in_service = Column(Integer, default=1, nullable=False)

class Bookings(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True)
    equipment_id = Column(Integer,ForeignKey("equipment.id"),nullable=False)
    roll_no = Column(String, nullable=False)
    booking_date = Column(Date, nullable=False)
    booked_on = Column(DateTime, default=datetime.now)
    cancelled = Column(Integer, default=0, nullable=False)

Base.metadata.create_all(engine)

def _equipment_response(item):
    return {
        "id": item.id,
        "name": item.name,
        "type": item.type,
        "lab_room": item.lab_room,
        "in_service": item.in_service
    }