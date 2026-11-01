from sqlalchemy import Integer, String, Column, create_engine,DateTime, ForeignKey
from sqlalchemy.orm import Session, declarative_base
from datetime import datetime,date

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
    roll_no = Column(String,nullable=False)
    registered_on = Column(DateTime,default=datetime.now)
    cancelled_on = Column(DateTime,nullable=True)
Base.metadata.create_all(engine)



def get_all_events(category= None):
    session = Session(engine)
    if category == None:
        events = session.query(Events).all()
    else:
        events = session.query(Events).filter(
            Events.category == category
        ).all()
        
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



def get_event(id):
    session = Session(engine)
    event = session.get(Events,id)

    if event is None:
        session.close()
        return None

    response = {
        "id":event.id,
        "title":event.title,
        "club":event.club,
        "category":event.category,
        "event_date":event.event_date,
        "total_seats":event.total_seats,
        "seats_left":event.seats_left

    }
    session.close()
    return response


def add_event(title,club,category,event_date,total_seats):
    session = Session(engine)
    event = Events(title=title,club=club,category=category,event_date=event_date,total_seats=total_seats,seats_left=total_seats)

    response = {"message": "Event added successfully"}
    session.add(event)
    session.commit()
    session.close()
    return response


def delete_event(event_id):
    session = Session(engine)
    event = session.get(Events,event_id)

    if event is None:
        session.close()
        return None
    registrations = session.query(Registrations).filter(
        Registrations.event_id == event_id,
        Registrations.cancelled_on == None
    ).all()
    if len(registrations) > 0:
        session.close()
        return {"error" : "This event has active registrations"}
    session.query(Registrations).filter(
        Registrations.event_id ==event_id

    ).delete()
    session.delete(event)
    session.commit()     
    session.close()
    return{"message":"Event deleted successfully"}
       

def register_student(event_id,roll_no):
    session = Session(engine)
    event = session.get(Events,event_id)
    if event is None:
        session.close()
        return None
    if event.seats_left <= 0:
        session.close()
        return{"error":"No seats available"}
    if date.fromisoformat(event.event_date) < date.today():
        session.close()
        return{"error":"Event has already passed"}
    registration = session.query(Registrations).filter(
        Registrations.event_id == event_id,
        Registrations.roll_no == roll_no,
        Registrations.cancelled_on == None
    ).first()
    if registration:
        session.close()
        return{"error":"Already registered"}
    registration = Registrations(event_id=event_id,roll_no= roll_no)
    session.add(registration)
    event.seats_left=event.seats_left - 1
    session.commit()
    session.close()
    return{"message":"Registration successful"}


def get_student_registrations(roll_no):
    session = Session(engine)

    registrations = session.query(Registrations).filter(
        Registrations.roll_no == roll_no,
        Registrations.cancelled_on == None
    ).all()
    response = []
    for registration in registrations:
        event = session.get(Events,registration.event_id)

        temp_item = {
            "registration_id": registration.id,
            "event_id": event.id,
            "title":event.title,
            "event_date":event.event_date
        }

        response.append(temp_item)
    session.close()
    return response
    
def cancel_registration(registration_id):
    session = Session(engine)
    registration = session.get(Registrations,registration_id)

    if registration is None:
        session.close()
        return None
    if registration.cancelled_on != None:
        session.close()
        return {"error":"Already cancelled"}
    registration.cancelled_on = datetime.now()
    event = session.get(Events,registration.event_id)
    event.seats_left = event.seats_left + 1
    session.commit()
    session.close()
    return {"message":"Registration cancelled successfully"}
  
