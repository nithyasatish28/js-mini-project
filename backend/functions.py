from sqlalchemy import Integer, String, Column, create_engine, ForeignKey, DateTime
from sqlalchemy.orm import Session, declarative_base
from datetime import date, timedelta
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


class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True)
    equipment_id = Column(Integer, ForeignKey("equipment.id"), nullable=False)
    roll_no = Column(String, nullable=False)
    booking_date = Column(String, nullable=False)
    booked_on = Column(DateTime, default=date.today)
    cancelled = Column(Integer, nullable=False, default=0)


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


def get_all_equipment(type=None):
    if type and type.strip() and type not in VALID_TYPES:
        raise HTTPException(
            status_code=422,
            detail="Type must be microscope, oscilloscope, 3d-printer, laptop or camera."
        )
    session = Session(engine)
    if not type or not type.strip():
        items = session.query(Equipment).all()
    else:
        items = session.query(Equipment).filter(Equipment.type == type).all()
    response = []
    for item in items:
        response.append({
            "id": item.id,
            "name": item.name,
            "type": item.type,
            "lab_room": item.lab_room,
            "in_service": item.in_service
        })
    session.close()
    return response


def get_equipment(id):
    session = Session(engine)
    item = session.get(Equipment, id)
    if item is None:
        session.close()
        raise HTTPException(status_code=404, detail="Equipment not found.")
    response = {
        "id": item.id,
        "name": item.name,
        "type": item.type,
        "lab_room": item.lab_room,
        "in_service": item.in_service
    }
    session.close()
    return response


def add_equipment(name, type, lab_room):
    if not name or not name.strip() or not lab_room or not lab_room.strip():
        raise HTTPException(status_code=422, detail="Name and lab room cannot be empty.")
    if type not in VALID_TYPES:
        raise HTTPException(
            status_code=422,
            detail="Type must be microscope, oscilloscope, 3d-printer, laptop or camera."
        )
    session = Session(engine)
    item = Equipment(name=name.strip(), type=type, lab_room=lab_room.strip(), in_service=1)
    session.add(item)
    session.commit()
    response = {
        "id": item.id,
        "name": item.name,
        "type": item.type,
        "lab_room": item.lab_room,
        "in_service": item.in_service
    }
    session.close()
    return response


def update_service(equipment_id, in_service):
    session = Session(engine)
    equipment = session.query(Equipment).filter(Equipment.id == equipment_id).first()

    if not equipment:
        session.close()
        raise HTTPException(status_code=404, detail="Equipment not found.")

    equipment.in_service = 1 if in_service else 0
    session.add(equipment)
    session.commit()
    session.close()


def add_booking(equipment_id, roll_no, booking_date, booked_on=None):
    roll_str = str(roll_no).strip() if roll_no is not None else ""
    if not roll_str:
        raise HTTPException(status_code=422, detail="Roll number is required.")

    if not booking_date or not str(booking_date).strip():
        raise HTTPException(status_code=422, detail="Booking date is required.")

    try:
        booking_date_obj = date.fromisoformat(str(booking_date).strip())
    except (ValueError, TypeError):
        raise HTTPException(status_code=422, detail="Date must be written as YYYY-MM-DD.")

    today = date.today()
    if booking_date_obj < today:
        raise HTTPException(status_code=422, detail="Booking date cannot be in the past.")

    if booking_date_obj > today + timedelta(days=7):
        raise HTTPException(status_code=422, detail="Booking date cannot be more than 7 days from today.")

    date_str = str(booking_date_obj)

    session = Session(engine)

    equipment = session.get(Equipment, equipment_id)
    if not equipment:
        session.close()
        raise HTTPException(status_code=404, detail="Equipment not found.")

    if not equipment.in_service:
        session.close()
        raise HTTPException(status_code=409, detail="This item is currently out of service.")

    existing_booking = session.query(Booking).filter(
        Booking.equipment_id == equipment_id,
        Booking.booking_date == date_str,
        Booking.cancelled == 0
    ).first()
    if existing_booking:
        session.close()
        raise HTTPException(status_code=409, detail="This item is already booked for that day.")

    student_bookings_count = session.query(Booking).filter(
        Booking.roll_no == roll_str,
        Booking.booking_date == date_str,
        Booking.cancelled == 0
    ).count()
    if student_bookings_count >= 2:
        session.close()
        raise HTTPException(status_code=409, detail="Student already has 2 bookings for that date.")

    booking = Booking(
        equipment_id=equipment_id,
        roll_no=roll_str,
        booking_date=date_str,
        booked_on=booked_on if booked_on else today,
        cancelled=0
    )
    session.add(booking)
    session.commit()
    response = {
        "id": booking.id,
        "equipment_id": booking.equipment_id,
        "roll_no": booking.roll_no,
        "booking_date": booking.booking_date,
        "booked_on": booking.booked_on,
        "cancelled": booking.cancelled
    }
    session.close()
    return response


def get_student_bookings(roll_no):
    roll_str = str(roll_no).strip() if roll_no is not None else ""
    if not roll_str:
        raise HTTPException(status_code=422, detail="Roll number is required.")

    session = Session(engine)

    has_booking = session.query(Booking).filter(Booking.roll_no == roll_str).first()
    if not has_booking:
        session.close()
        raise HTTPException(status_code=404, detail="This roll number doesn't have any bookings.")

    today_str = str(date.today())

    results = session.query(Booking, Equipment).join(
        Equipment, Booking.equipment_id == Equipment.id
    ).filter(
        Booking.roll_no == roll_str,
        Booking.booking_date >= today_str
    ).all()

    response = []
    for booking, eq in results:
        response.append({
            "id": booking.id,
            "equipment_id": booking.equipment_id,
            "equipment_name": eq.name,
            "roll_no": booking.roll_no,
            "booking_date": booking.booking_date,
            "booked_on": booking.booked_on,
            "cancelled": booking.cancelled
        })

    session.close()
    return response


def cancel_booking(booking_id):
    session = Session(engine)
    booking = session.query(Booking).filter(Booking.id == booking_id).first()

    if not booking:
        session.close()
        raise HTTPException(status_code=404, detail="Booking not found.")

    if booking.cancelled == 1:
        session.close()
        raise HTTPException(status_code=409, detail="Booking is already cancelled.")

    booking.cancelled = 1
    session.add(booking)
    session.commit()
    session.close()
    return {"message": "Booking cancelled successfully."}
