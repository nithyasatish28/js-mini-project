from sqlalchemy import Integer, String, Column, create_engine, ForeignKey, DateTime
from sqlalchemy.orm  import Session, declarative_base
from datetime import  date
from fastapi import  HTTPException

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
    booked_on = Column(DateTime, default=date.today())
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

# E1
def get_all_equipment(type = None):
    session = Session(engine)
    if type is None:
        items = session.query(Equipment).all()
    else:
        items = session.query(Equipment).filter(Equipment.type == type).all()
    response = []
    for item in items:
        temp_item = {
            "id" : item.id,
            "name" : item.name,
            "type" : item.type,
            "lab_room" : item.lab_room,
            "in_service" : item.in_service
        }
        response.append(temp_item)
    session.close()
    return response


# E2
def get_equipment(id):
    session = Session(engine)
    item = session.get(Equipment, id)
    if item is None:
        session.close()
        raise HTTPException(status_code=404, detail="Equipment not found.")
    response = {
        "id" : item.id,
        "name" : item.name,
        "type" : item.type,
        "lab_room" : item.lab_room,
        "in_service" : item.in_service
    }
    session.close()
    return response


# E3
def add_equipment(name, type, lab_room):
    session = Session(engine)
    item = Equipment(name = name, type = type, lab_room = lab_room, in_service = 1)
    session.add(item)
    session.commit()
    response = {
        "id" : item.id,
        "name" : item.name,
        "type" : item.type,
        "lab_room" : item.lab_room,
        "in_service" : item.in_service
    }
    session.close()
    return response

#E4
def update_service( equipment_id, in_service):
    session = Session(engine)
    equipment = session.query(Equipment).filter(Equipment.id == equipment_id).first()

    if equipment:
        equipment.in_service = in_service
        session.add(equipment)
        session.commit()
        session.close()


#E5
def add_booking(equipment_id, roll_no, booking_date, booked_on=date.today()):
        session = Session(engine)
        booking = Booking(equipment_id=equipment_id, roll_no=roll_no, booking_date=booking_date,booked_on=booked_on)
        session.add(booking)
        response =  {
            "id": booking.id,
            "equipment_id": booking.equipment_id,
            "roll_no": booking.roll_no,
            "booking_date": booking.booking_date,
            "booked_on": booking.booked_on,
            "cancelled": booking.cancelled
        }
        session.commit()
        session.close()
        return response


#E6
def get_student_bookings(roll_no):
    session = Session(engine)
    bookings = session.query(Booking).filter(Booking.roll_no == roll_no).all()
    response = []
    for booking in bookings:
        # today = date.today()
        # if booking.booking_date >= today:
            temp_booking = {
                "id" : booking.id,
                "equipment_id": booking.equipment_id,
                "roll_no": booking.roll_no,
                "booking_date": booking.booking_date,
                "booked_on": booking.booked_on,
                "cancelled": booking.cancelled
            }
            response.append(temp_booking)

    session.close()
    return response

#E7
def cancel_booking(booking_id):
    session = Session(engine)
    booking = session.query(Booking).filter(Booking.id == booking_id).first()
    if booking:
        booking.cancelled = True
        session.add(booking)
        session.commit()
        session.close()

    session.close()
    return booking

