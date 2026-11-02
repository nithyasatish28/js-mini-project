from datetime import date
from sqlalchemy import Column, Date, Integer, ForeignKey, String, create_engine
from sqlalchemy.orm import declarative_base, Session

DB_PATH = "lab.db"
engine = create_engine(f"sqlite:///{DB_PATH}")
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

equipment_types = [
    "microscope",
    "oscilloscope",
    "3d-printer",
    "laptop",
    "camera"
]


def get_all_equipments(equipment_type=None):
    session = Session(engine)

    if equipment_type:
        equipments = session.query(Equipment).filter(
            Equipment.type == equipment_type
        ).all()
    else:
        equipments = session.query(Equipment).all()

    response = []

    for equipment in equipments:
        response.append({
            "id": equipment.id,
            "name": equipment.name,
            "type": equipment.type,
            "lab_room": equipment.lab_room,
            "in_service": equipment.in_service
        })

    session.close()
    return response


def get_equipment_by_type(equipment_type):
    session = Session(engine)

    equipments = session.query(Equipment).filter(
        Equipment.type == equipment_type
    ).all()

    response = []

    for equipment in equipments:
        response.append({
            "id": equipment.id,
            "name": equipment.name,
            "type": equipment.type,
            "lab_room": equipment.lab_room,
            "in_service": equipment.in_service
        })

    session.close()
    return response


def get_equipment_by_id(equipment_id):
    session = Session(engine)

    equipment = session.get(Equipment, equipment_id)

    if equipment is None:
        session.close()
        return None

    response = {
        "id": equipment.id,
        "name": equipment.name,
        "type": equipment.type,
        "lab_room": equipment.lab_room,
        "in_service": equipment.in_service
    }

    session.close()
    return response


def add_equipment(name, equipment_type, lab_room):
    session = Session(engine)

    equipment = Equipment(
        name=name,
        type=equipment_type,
        lab_room=lab_room,
        in_service=1
    )

    session.add(equipment)
    session.commit()
    session.refresh(equipment)

    response = {
        "id": equipment.id,
        "name": equipment.name,
        "type": equipment.type,
        "lab_room": equipment.lab_room,
        "in_service": equipment.in_service
    }

    session.close()
    return response


def update_service(equipment_id, in_service):
    session = Session(engine)

    equipment = session.get(Equipment, equipment_id)

    if equipment is None:
        session.close()
        return None

    equipment.in_service = int(in_service)

    session.commit()
    session.refresh(equipment)

    response = {
        "id": equipment.id,
        "name": equipment.name,
        "type": equipment.type,
        "lab_room": equipment.lab_room,
        "in_service": equipment.in_service
    }

    session.close()
    return response


def book_equipment(equipment_id, roll_no, booking_date):
    session = Session(engine)

    equipment = session.query(Equipment).filter(
        Equipment.id == equipment_id
    ).first()

    if equipment is None:
        session.close()
        return None

    if equipment.in_service == 0:
        session.close()
        return "out_of_service"

    booking = session.query(Bookings).filter(
        Bookings.equipment_id == equipment_id,
        Bookings.booking_date == booking_date,
        Bookings.cancelled == 0
    ).first()

    if booking is not None:
        session.close()
        return "already_booked"

    count = session.query(Bookings).filter(
        Bookings.roll_no == roll_no,
        Bookings.booking_date == booking_date,
        Bookings.cancelled == 0
    ).count()

    if count >= 2:
        session.close()
        return "booking_limit"

    booking = Bookings(
        equipment_id=equipment_id,
        roll_no=roll_no,
        booking_date=booking_date,
        booked_on=date.today(),
        cancelled=0
    )

    session.add(booking)
    session.commit()
    session.refresh(booking)

    response = {
        "id": booking.id,
        "equipment_id": booking.equipment_id,
        "equipment_name": equipment.name,
        "roll_no": booking.roll_no,
        "booking_date": booking.booking_date.isoformat(),
        "booked_on": booking.booked_on.isoformat(),
        "cancelled": booking.cancelled
    }

    session.close()
    return response


def get_student_bookings(roll_no):
    session = Session(engine)

    bookings = session.query(Bookings).filter(
        Bookings.roll_no == roll_no,
        Bookings.cancelled == 0,
        Bookings.booking_date >= date.today()
    ).all()

    response = []

    for booking in bookings:
        equipment = session.get(Equipment, booking.equipment_id)

        response.append({
            "id": booking.id,
            "equipment_id": booking.equipment_id,
            "equipment_name": equipment.name,
            "roll_no": booking.roll_no,
            "booking_date": booking.booking_date.isoformat(),
            "booked_on": booking.booked_on.isoformat(),
            "cancelled": booking.cancelled
        })

    session.close()
    return response


def get_booking(booking_id):
    session = Session(engine)

    booking = session.query(Bookings).filter(
        Bookings.id == booking_id
    ).first()

    session.close()
    return booking


def cancel_booking(booking_id):
    session = Session(engine)

    booking = session.query(Bookings).filter(
        Bookings.id == booking_id
    ).first()

    if booking is None:
        session.close()
        return None

    equipment = session.get(Equipment, booking.equipment_id)

    booking.cancelled = 1

    session.commit()
    session.refresh(booking)

    response = {
        "id": booking.id,
        "equipment_id": booking.equipment_id,
        "equipment_name": equipment.name,
        "roll_no": booking.roll_no,
        "booking_date": booking.booking_date.isoformat(),
        "booked_on": booking.booked_on.isoformat(),
        "cancelled": booking.cancelled
    }

    session.close()
    return response
