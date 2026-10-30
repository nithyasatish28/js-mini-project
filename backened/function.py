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

def get_all_event(category:str):
        session = Session(engine)
        events = session.query(Event).all()
        response = []
        for event in events:
             temp_event= {
        "id": events.id,
        "title": events.title,
        "club":events.club,
        "category": events.category,
        "event_date":events.event_date,
        "total_seats":events.total_seats,
        "seats_left":events.seats_left
        }
            
        session.close()
        return response

    
                                              
def get_event(id):
    session= Session(engine)
    events= session.get(Event, id)
    response = { "id": events.id,
             "title": events.title,
            "club":events.club,
            "category": events.category,
            "event_date":events.event_date,
            "total_seats":events.total_seats,
            "seats_left":events.seats_left
            }
    session.close()
    return response


def add_new_event(title: str, club: str, category: str, events_date:str,total_seats:int):
    session = Session(engine)  
    events = session.add(title=title, club=club, category=category, events_date=events_date ,total_seats=total_seats ,seats_left=total_seats)
    response = { "title"=events.title,
                 "club"= events.club, 
                 "events_date"= events.events_date ,
                 "total_seats"=events.total_seats

    }
    session.close()
    return response

def delete_event(event_id):
 session = Session(engine)  
 events = session.get(Event,event_id)
 session.delete(events)
 session.commit
 session.close
