from datetime import datetime
from datetime import date 
from sqlalchemy import Column, DateTime,Date, Integer, ForeignKey, String, create_engine
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
    booking_date = Column(Date, nullable=False)
    booked_on = Column(Date, nullable=False)
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

def booking_response(booking, equipment_name=None):
    return {
        "id": booking.id,
        "equipment_id": booking.equipment_id,
        "equipment_name": equipment_name,
        "roll_no": booking.roll_no,
        "booking_date": booking.booking_date.isoformat(),
        "booked_on": booking.booked_on.isoformat(),
        "cancelled": booking.cancelled
    }

def get_all_equipments(equipment_type=None):
    with SessionLocal() as db:
        if equipment_type:
            equipment = db.query(Equipment).filter(
                Equipment.type == equipment_type).all()
        else:
            equipment = db.query(Equipment).all()

        return [equipment_response(item) for item in equipment]

def get_equipment_by_type(equipment_type):
    with SessionLocal() as db:
        equipment_list = db.query(Equipment).filter(
            Equipment.type == equipment_type
        ).all()

        return equipment_list
    
def get_equipment_by_id(equipment_id):
    with SessionLocal() as db:
        equipment = db.get(Equipment, equipment_id)

        if equipment is not None:
            return equipment_response(equipment)

        return None


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
    

def update_service(equipment_id, in_service):
    with SessionLocal() as db:
        equipment = db.get(Equipment, equipment_id)

        if equipment is not None:
            equipment.in_service = int(in_service)
            db.commit()
            db.refresh(equipment)

            return equipment_response(equipment)
        return None

def book_equipment(equipment_id, roll_no, booking_date):

    with SessionLocal() as db:

        equipment = db.get(Equipment, equipment_id)

        if equipment is None:
            return None

        if equipment.in_service == 0:
            return "out_of_service"

        booking = db.query(Bookings).filter(
            Bookings.equipment_id == equipment_id,
            Bookings.booking_date == booking_date,
            Bookings.cancelled == 0
        ).first()

        if booking is not None:
            return "already_booked"

        count = db.query(Bookings).filter(
            Bookings.roll_no == roll_no,
            Bookings.booking_date == booking_date,
            Bookings.cancelled == 0
        ).count()

        if count >= 2:
            return "booking_limit"

        new_booking = Bookings(
            equipment_id=equipment_id,
            roll_no=roll_no,
            booking_date=booking_date,
            booked_on=date.today(),
            cancelled=0
        )

        db.add(new_booking)
        db.commit()
        db.refresh(new_booking)

        return booking_response(new_booking, equipment.name)