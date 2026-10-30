from sqlalchemy import Integer,String, Column, create_engine, DateTime,ForeignKey
from sqlalchemy.orm import Session, declarative_base
from datetime import datetime

DB_PATH="event.db"
engine = create_engine(f"sqlite:///{DB_PATH}")
Base = declarative_base()

class Event (Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True )
    title = Column(String)
    club = Column(String)
    category = Column(String)
    event_date = Column(DateTime , default=datetime.now)  
    total_seats= Column(Integer)
    seats_left= Column(Integer)

    
class Registration(Base):
    __tablename__ = "registrations"
    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey("events.id"))
    roll_no = Column(Integer)
    registered_on = Column(DateTime , default=datetime.now)
    cancelled_on = Column(DateTime,nullable=True )  

Base.metadata.create_all(engine)

def add_all_event( title: str, club: str, category:str,):
        with Session(engine) as session:
            events = Event( title=title,club=club,category=category)
            session.add(events)
            response={ "title": Event.title, "club": Event.club, "category": Event.category}
            session.commit()
            session.close()
            return response                                             
        