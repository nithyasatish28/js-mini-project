from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, create_engine
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


class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True)
    equipment_id = Column(Integer, ForeignKey("equipment.id"), nullable=False)
    roll_no = Column(String, nullable=False)
    booking_date = Column(String, nullable=False)
    booked_on = Column(DateTime, default=datetime.utcnow)
    cancelled = Column(Integer, nullable=False, default=0)


Base.metadata.create_all(engine)

session = SessionLocal()
if session.query(Equipment).first() is None:
    session.add_all(
        [
            Equipment(name="Lab Microscope 1", type="microscope", lab_room="Lab 101"),
            Equipment(name="Lab Microscope 2", type="microscope", lab_room="Lab 101"),
            Equipment(name="Oscilloscope 1", type="oscilloscope", lab_room="Lab 202"),
            Equipment(name="Oscilloscope 2", type="oscilloscope", lab_room="Lab 202"),
            Equipment(name="3D Printer", type="3d-printer", lab_room="Workshop"),
            Equipment(name="Lab Laptop 1", type="laptop", lab_room="Lab 105"),
            Equipment(name="Lab Laptop 2", type="laptop", lab_room="Lab 105"),
            Equipment(name="Camera 1", type="camera", lab_room="Media Room"),
            Equipment(name="Camera 2", type="camera", lab_room="Media Room"),
            Equipment(
                name="Lab Microscope 3",
                type="microscope",
                lab_room="Lab 101",
                in_service=0,
            ),
        ]
    )
    session.commit()
session.close()
