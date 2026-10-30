from sqlalchemy import Integer, String, Column, create_engine
from sqlalchemy.orm  import Session, declarative_base
from datetime import datetime
from fastapi import HTTPException 

DB_PATH = "lab.db"
engine = create_engine(f"sqlite:///{DB_PATH}")
Base = declarative_base()

VALID_TYPES = ["microscope", "oscilloscope", "3d-printer", "laptop", "camera"]


class Equipment(Base):
    _tablename_ = "equipment"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    type = Column(String)
    lab_room = Column(String)
    in_service = Column(Integer, default=1)


class Bookings(Base):
    _tablename_ = "bookings"
    id = Column(Integer, primary_key=True)
    equipment_id = Column(Integer)
    roll_no = Column(String)
    booking_date = Column(String)
    booked_on = Column(String)
    cancelled = Column(Integer, default=0)


Base.metadata.create_all(engine)