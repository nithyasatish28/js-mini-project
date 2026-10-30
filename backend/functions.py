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
equipment_types = ["microscope", "oscilloscope", "3d-printer", "laptop", "camera"]

def equipment_response(equipment):

    return {
        "id": equipment.id,
        "name": equipment.name,
        "type": equipment.type,
        "lab_room": equipment.lab_room,
        "in_service": equipment.in_service
    }

def get_all_equipments(equipment_type=None):
    with SessionLocal() as db:
        if equipment_type:
            equipment = db.query(Equipment).filter(
                Equipment.type == equipment_type).all()
        else:
            equipment = db.query(Equipment).all()

        return [equipment_response(equipment) for item in equipment]
    
    
def add_equipment(name, equipment_type, lab_room):
    with SessionLocal() as db:
        equipment = Equipment(
            name=name,
            type=equipment_type,
            lab_room=lab_room,
            in_service=1
        )

        db.add(equipment)
        db.commit()
        db.refresh(equipment)

        return equipment_response(equipment)