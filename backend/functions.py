
from sqlalchemy import (
    Integer, String, Column, create_engine,
    DateTime, ForeignKey
)
from sqlalchemy.orm import Session, declarative_base
from datetime import datetime, date



DB_PATH = "events.db"

engine = create_engine(f"sqlite:///{DB_PATH}")

Base = declarative_base()


# table 1

class Events(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    club = Column(String, nullable=False)
    category = Column(String, nullable=False)
    event_date = Column(String, nullable=False)
    total_seats = Column(Integer, nullable=False)
    seats_left = Column(Integer, nullable=False)


# table 2

class Registrations(Base):
    __tablename__ = "registrations"
    id = Column(Integer, primary_key=True)
    event_id = Column(Integer,ForeignKey("events.id"),nullable=False)
    roll_no = Column(String, nullable=False)
    registered_on = Column(DateTime, default=datetime.now)
    cancelled_on = Column(DateTime, nullable=True)




Base.metadata.create_all(engine)


# events

def seed_events():
    session = Session(engine)

    if session.query(Events).count() == 0:

        initial_events = [
            Events(
                title="Python Workshop",
                club="Coding Club",
                category="technical",
                event_date="2026-11-05",
                total_seats=50,
                seats_left=50
            ),
            Events(
                title="Cultural Fest",
                club="Cultural Club",
                category="cultural",
                event_date="2026-11-10",
                total_seats=100,
                seats_left=100
            ),
            Events(
                title="Football Tournament",
                club="Sports Club",
                category="sports",
                event_date="2026-11-15",
                total_seats=40,
                seats_left=0
            ),
            Events(
                title="AI Seminar",
                club="Tech Club",
                category="seminar",
                event_date="2026-11-20",
                total_seats=60,
                seats_left=60
            ),
            Events(
                title="Web Development Workshop",
                club="Coding Club",
                category="workshop",
                event_date="2026-11-25",
                total_seats=30,
                seats_left=30
            ),
            Events(
                title="Dance Competition",
                club="Cultural Club",
                category="cultural",
                event_date="2026-12-01",
                total_seats=80,
                seats_left=80
            ),
            Events(
                title="Cricket Tournament",
                club="Sports Club",
                category="sports",
                event_date="2026-12-05",
                total_seats=50,
                seats_left=50
            ),
            Events(
                title="Python Introduction",
                club="Coding Club",
                category="technical",
                event_date="2026-10-01",
                total_seats=40,
                seats_left=40
            )
        ]

        session.add_all(initial_events)
        session.commit()

    session.close()


seed_events()




def get_all_events(category=None):

    session = Session(engine)

    if category is None:
        events = session.query(Events).all()
    else:
        events = session.query(Events).filter(
            Events.category == category
        ).all()

    response = []

    for event in events:

        temp_item = {
            "id": event.id,
            "title": event.title,
            "club": event.club,
            "category": event.category,
            "event_date": event.event_date,
            "total_seats": event.total_seats,
            "seats_left": event.seats_left
        }

        response.append(temp_item)

    session.close()

    return response




def get_event(id):

    session = Session(engine)

    event = session.get(Events, id)

    if event is None:
        session.close()
        return None

    response = {
        "id": event.id,
        "title": event.title,
        "club": event.club,
        "category": event.category,
        "event_date": event.event_date,
        "total_seats": event.total_seats,
        "seats_left": event.seats_left
    }

    session.close()

    return response




def add_event(title, club, category, event_date, total_seats):

    session = Session(engine)

    event = Events(
        title=title,
        club=club,
        category=category,
        event_date=event_date,
        total_seats=total_seats,
        seats_left=total_seats
    )

    session.add(event)
    session.commit()

    response = {"message": "Event added successfully", "event_id": event.id }

    session.close()

    return response




def delete_event(event_id):

    session = Session(engine)

    event = session.get(Events, event_id)

    if event is None:
        session.close()
        return None

    registrations = session.query(Registrations).filter(
        Registrations.event_id == event_id,
        Registrations.cancelled_on.is_(None)
    ).all()

    if len(registrations) > 0:
        session.close()

        return {"error": "This event has active registrations"}

    # Delete old cancelled registrations first

    session.query(Registrations).filter(
        Registrations.event_id == event_id
    ).delete(synchronize_session=False)

    session.delete(event)
    session.commit()
    session.close()

    return {"message": "Event deleted successfully"}




def register_student(event_id, roll_no):

    session = Session(engine)

    event = session.get(Events, event_id)

    if event is None:
        session.close()
        return None

    # CHECK SEATS

    if event.seats_left <= 0:
        session.close()

        return {
            "error": "This event is full."
        }

    # CHECK EVENT DATE

    if date.fromisoformat(event.event_date) < date.today():
        session.close()

        return {"error": "Event has already passed."}

    # CHECK DUPLICATE REGISTRATION

    registration = session.query(Registrations).filter(
        Registrations.event_id == event_id,
        Registrations.roll_no == roll_no,
        Registrations.cancelled_on.is_(None)
    ).first()

    if registration:
        session.close()

        return {"error": "Already registered for this event."}

    # CREATE REGISTRATION

    registration = Registrations(
        event_id=event_id,
        roll_no=roll_no
    )

    session.add(registration)

    #  DECREASE AVAILABLE SEATS

    event.seats_left -= 1

    session.commit()

    response = { "message": "Registration successful", "registration_id": registration.id}

    session.close()

    return response



def get_student_registrations(roll_no):

    session = Session(engine)

    registrations = session.query(Registrations).filter(
        Registrations.roll_no == roll_no,
        Registrations.cancelled_on.is_(None)
    ).all()

    response = []

    for registration in registrations:

        event = session.get(Events, registration.event_id)

        if event is None:
            continue

        temp_item = {
            "registration_id": registration.id,
            "event_id": event.id,
            "title": event.title,
            "event_date": event.event_date
        }

        response.append(temp_item)

    session.close()

    return response



def cancel_registration(registration_id):

    session = Session(engine)

    registration = session.get(
        Registrations,
        registration_id
    )

    if registration is None:
        session.close()
        return None

    # CHECK ALREADY CANCELLED

    if registration.cancelled_on is not None:
        session.close()

        return {
            "error": "Registration already cancelled."
        }

    # UPDATE CANCELLATION DATE

    registration.cancelled_on = datetime.now()

    event = session.get(Events, registration.event_id)

    # INCREASE AVAILABLE SEATS , this is optional check again

    if event is not None:
        event.seats_left += 1

    session.commit()
    session.close()

    return {
        "message": "Registration cancelled successfully"
    }



