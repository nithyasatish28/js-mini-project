from sqlalchemy import Integer,String, Column, create_engine, DateTime,ForeignKey
from sqlalchemy.orm import Session, declarative_base
from datetime import datetime , date

DB_PATH="event.db"
engine = create_engine(f"sqlite:///{DB_PATH}")
Base = declarative_base()

Categories = ["technical", "cultural"," sports", "workshop", "seminar"]

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
            "id": event.id,
            "title": event.title,
            "club":event.club,
            "category": event.category,
            "event_date":event.event_date,
            "total_seats":event.total_seats,
            "seats_left":event.seats_left
        }
        response.append(temp_event)
        
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




def add_new_event(title: str, club: str, category: str, events_date:datetime,total_seats:int):
    session = Session(engine)  
    events = session.add(title=title, club=club, category=category, events_date=events_date ,total_seats=total_seats ,seats_left=total_seats)

    response = {
        "title": event.title,
        "club": event.club,
        "event_date": event.event_date,
        "total_seats":event.total_seats
    }
    session.commit()
    session.close()
    return response

def delete_event(event_id):
 session = Session(engine)  
 events = session.get(Event,event_id)

 if events:
    session.delete(events)
    session.commit
    session.close



def event_roll_number(event_id: int, roll_number:int):
     session = session(engine)
     event = session.get(Event, event_id)
     if not event:
         return{"error:event not found"}
     
     if event.seats_left <=0:
         return{"error:The seats are full"}

     registration = Registration(
                event_id = event_id,
                roll_number = roll_number,
                registration_date = date.today()
            )

     return{
         "registration_id" : registration.id,
         "event_id" : event.id,
         "roll_number" : registration.roll_number,
         "registration_date" : registration.registration_date,
         "seats_left" : event.seats_left,
}


def student_registration(title: str, club: str, category:str, event_date: int, total_seats: int):
    session = session(engine)

event = Event(
        title=title,
        club=club,
        category=category,
        event_date=event_date,
        total_seats=total_seats,
        seats_left=total_seats,
     )
    session.add(event)
    session.commit()
    session.refresh(event)

response {
    
         "id": event.id,
        "title": event.title,
        "club": event.club,
        "event_date": event.event_date,
        "total_seats": event.total_seats,
        "seats_left": event.seats_left,
    }

        session.close()
        return response
}

 def get_event(event_id: int):
     session = Session(engine)
 
     event = session.get(Event, event_id)
     if not event:
         session.close()
         return {"error": "Event not found"}
 
     response = {
         "id": event.id,
         "title": event.title,
         "club": event.club,
         "event_date": event.event_date,
         "seats_left": event.seats_left,
     }
 
     session.close()
     return response
    
