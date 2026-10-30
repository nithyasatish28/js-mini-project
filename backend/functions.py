from sqlalchemy import Integer, String, Column, create_engine,DateTime, ForeignKey
from sqlalchemy.orm import Session, declarative_base
from datetime import datetime

DB_PATH = "events.db"
engine = create_engine(f"sqlite:///{DB_PATH}")
Base = declarative_base()


class Events(Base):
    __tablename__ = "events"

    id = Column(Integer,primary_key=True)
    title = Column(String)
    club = Column(String)
    category = Column(String)
    event_date = Column(String)
    total_seats = Column(Integer)
    seats_left = Column(Integer)


class Registrations(Base):
    __tablename__ = "registrations"
    id = Column(Integer,primary_key=True)
    event_id = Column(Integer,ForeignKey("events.id"),nullable=False)
    registered_on = Column(DateTime,default=datetime.now)
    cancelled_on = Column(DateTime,nullable=True)
Base.metadata.create_all(engine)



def get_all_events():
    session = Session(engine)
    events = session.query(Events).all()
    response =[]

    for event in events:
        temp_item = {
        "id": event.id,
        "title": event.title,
        "club":event.club,
        "category": event.category,
        "event_date":event.event_date,
        "total_seats":event.total_seats,
        "seats_left":event.seats_left
        }
        response.append(temp_item)
    session.close()
    return response
