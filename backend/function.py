from datetime import datetime, date

from sqlalchemy import (Column,Date,DateTime,ForeignKey,Integer,String,create_engine,)
from sqlalchemy.orm import declarative_base, sessionmaker

session_PATH = "lab.session"

engine = create_engine(f"sqlite:///{session_PATH}")
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

VALID_TYPES = ["microscope","oscilloscope","3d-printer","laptop","camera"]

class Equipment(Base):
    _tablename_ = "equipment"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    lab_room = Column(String, nullable=False)
    in_service = Column(Integer, default=1, nullable=False)

class Bookings(Base):
    _tablename_ = "bookings"
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
       

def _booking_response(booking, equipment_name=None):
    return {
        "id": booking.id,
        "equipment_id": booking.equipment_id,
        "equipment_name": equipment_name,
        "roll_no": booking.roll_no,
        "booking_date": booking.booking_date,
        "booking_on": booking.booking_on,
        "cancelled": booking.cancelled
    }

def add_initial_equipment():
    with SessionLocal() as session:
        if session.query(Equipment).count() == 0:

            equipment_list = [
                ("Digital Microscope", "microscope", "Lab 101", 1),
                ("Advanced Microscope", "microscope", "Lab 102", 1),
                ("Digital Oscilloscope", "oscilloscope", "Lab 201", 1),
                ("Analog Oscilloscope", "oscilloscope", "Lab 202", 1),
                ("3D Printer A", "3d-printer", "Lab 301", 1),
                ("3D Printer B", "3d-printer", "Lab 301", 0),
                ("Dell Laptop", "laptop", "Lab 401", 1),
                ("HP Laptop", "laptop", "Lab 402", 1),
                ("Canon Camera", "camera", "Lab 501", 1),
                ("Sony Camera", "camera", "Lab 502", 1)
            ]

            for name, type, room, status in equipment_list:
                item = Equipment( name=name, type=type, lab_room=room, in_service=status )
                session.add(item)
            session.commit()

def get_all_equipment(type=None):
    with SessionLocal() as session:
        query = session.query(Equipment)
        if type is not None:
            query = query.filter(Equipment.type == type)
        items = query.all()
        return [_equipment_response(item) for item in items]


def get_equipment(id):
    with SessionLocal() as session:
        item = session.get(Equipment, id)
        if item is None:
            return None
        return _equipment_response(item)


def add_equipment(name, type, lab_room):
    with SessionLocal() as session:
        item = Equipment( name=name, type=type, lab_room=lab_room, in_service=1 )
        session.add(item)
        session.commit()
        session.refresh(item)
        return _equipment_response(item)


def update_service(id, in_service):
    with SessionLocal() as session:
        item = session.get(Equipment, id)
        if item is None:
            return None
        item.in_service = in_service
        session.commit()
        session.refresh(item)
        return _equipment_response(item)


def book_equipment(equipment_id, roll_no, booking_date):
    with SessionLocal() as session:
        item = session.get(Equipment, equipment_id)
        if item is None:
            return {"error": 404, "detail": "Equipment not found."}
        if item.in_service == 0:
            return {"error": 409,"detail": "This item is out of service."}
        try:
            selected_date = date.fromisoformat(booking_date)
        except (ValueError, TypeError):
            return {"error": 422,"detail": "Date must be in YYYY-MM-DD format."}
        
        today = date.today()
        last_date = today + timedelta(days=7)
        if selected_date < today or selected_date > last_date:
            return {"error": 422,"detail": "Booking date must be within the next 7 days."}
        
        existing_booking = session.query(Bookings).filter(
            Bookings.equipment_id == equipment_id,
            Bookings.booking_date == selected_date,
            Bookings.cancelled == 0
        ).first()
        if existing_booking:
            return {"error": 409,"detail": "This item is already booked for that day."}
        
        student_bookings = session.query(Bookings).filter(
            Bookings.roll_no == roll_no,
            Bookings.booking_date == selected_date,
            Bookings.cancelled == 0
        ).count()
        if student_bookings >= 2:
            return {"error": 409,"detail": "You can only book 2 items per day."}
        
        booking = Bookings(
            equipment_id=equipment_id,
            roll_no=roll_no,
            booking_date=selected_date,
            booked_on=datetime.now(),
            cancelled=0
        )

        session.add(booking)
        session.commit()
        session.refresh(booking)
        return _booking_response(booking, item.name)
