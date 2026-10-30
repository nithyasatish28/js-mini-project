from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, ForeignKey, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DB_PATH = "lab.db"
engine = create_engine(f"sqlite:///{DB_PATH}")
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Equipment(Base):
    __tablename__ = "equipment"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    lab_room = Column(String, nullable=False)
    in_service = Column(Integer, nullable=False, default=1)

class Bookings(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True)
    equipment_id = Column(Integer, ForeignKey("equipment.id"), nullable=False)
    roll_no = Column(String, nullable=False)
    booking_date = Column(DateTime, nullable=False)
    booked_on = Column(DateTime, nullable=False)
    cancelled = Column(Integer, nullable=False, default=0)
Base.metadata.create_all(engine)

def equipment_response(equipment):

    return {
        "id": equipment.id,
        "name": equipment.name,
        "type": equipment.type,
        "lab_room": equipment.lab_room,
        "in_service": equipment.in_service
    }

