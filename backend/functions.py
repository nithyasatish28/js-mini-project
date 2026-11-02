from sqlalchemy import Integer, String, Column, create_engine, DateTime, ForeignKey
from sqlalchemy.orm import Session, declarative_base
from datetime import datetime, date

DB_PATH = "events.db"
engine = create_engine(f"sqlite:///{DB_PATH}")
Base = declarative_base()


class Events(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    club = Column(String, nullable=False)
    category = Column(String, nullable=False)
    event_date = Column(String, nullable=False)
    total_seats = Column(Integer, nullable=False)
    seats_left = Column(Integer, nullable=False)


class Registrations(Base):
    __tablename__ = "registrations"

    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    roll_no = Column(String, nullable=False)
    registered_on = Column(DateTime, default=datetime.now)
    cancelled_on = Column(DateTime, nullable=True)


# Create tables if they do not exist
Base.metadata.create_all(engine)


def seed_events():
    """Seed 8 initial events if database table is empty."""
    session = Session(engine)
    if session.query(Events).count() == 0:
        initial_events = [
            Events(
                title="Python Workshop",
                club="Coding Club",
                category="technical",
                event_date="2026-11-15",
                total_seats=50,
                seats_left=50
            ),
            Events(
                title="Cultural Fest",
                club="Cultural Club",
                category="cultural",
                event_date="2026-11-20",
                total_seats=100,
                seats_left=100
            ),
            Events(
                title="Football Tournament",
                club="Sports Club",
                category="sports",
                event_date="2026-11-22",
                total_seats=40,
                seats_left=0  # 0 seats left as required by PRD
            ),
            Events(
                title="AI Seminar",
                club="Tech Club",
                category="seminar",
                event_date="2026-11-25",
                total_seats=60,
                seats_left=60
            ),
            Events(
                title="Web Development Workshop",
                club="Coding Club",
                category="workshop",
                event_date="2026-11-28",
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
                event_date="2026-10-01",  # Date has already passed as required by PRD
                total_seats=40,
                seats_left=40
            )
        ]
        session.add_all(initial_events)
        session.commit()
    session.close()


seed_events()


# E1: GET ALL EVENTS (optionally filtered by category)
def get_all_events(category=None):
    session = Session(engine)
    if category:
        events = session.query(Events).filter(Events.category == category).all()
    else:
        events = session.query(Events).all()

    result = []
    for event in events:
        result.append({
            "id": event.id,
            "title": event.title,
            "club": event.club,
            "category": event.category,
            "event_date": event.event_date,
            "total_seats": event.total_seats,
            "seats_left": event.seats_left
        })
    session.close()
    return result


# E2: GET ONE EVENT
def get_event(event_id):
    session = Session(engine)
    event = session.get(Events, event_id)
    if event is None:
        session.close()
        return None

    result = {
        "id": event.id,
        "title": event.title,
        "club": event.club,
        "category": event.category,
        "event_date": event.event_date,
        "total_seats": event.total_seats,
        "seats_left": event.seats_left
    }
    session.close()
    return result


# E3: ADD EVENT
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
    event_id = event.id
    session.close()

    return {
        "message": "Event added successfully",
        "event_id": event_id
    }


# E4: DELETE EVENT
def delete_event(event_id):
    session = Session(engine)
    event = session.get(Events, event_id)
    if event is None:
        session.close()
        return None

    # Check for active (not cancelled) registrations
    active_regs = session.query(Registrations).filter(
        Registrations.event_id == event_id,
        Registrations.cancelled_on.is_(None)
    ).all()

    if len(active_regs) > 0:
        session.close()
        return {"error": "Cannot delete event with active registrations"}

    # Delete any past cancelled registrations for this event
    session.query(Registrations).filter(
        Registrations.event_id == event_id
    ).delete(synchronize_session=False)

    session.delete(event)
    session.commit()
    session.close()

    return {"message": "Event deleted successfully"}


# E5: REGISTER STUDENT
def register_student(event_id, roll_no):
    session = Session(engine)
    event = session.get(Events, event_id)
    if event is None:
        session.close()
        return None

    # Check if event has 0 seats left
    if event.seats_left <= 0:
        session.close()
        return {"error": "This event is full."}

    # Check if event date has already passed
    try:
        if date.fromisoformat(event.event_date) < date.today():
            session.close()
            return {"error": "Event has already passed."}
    except ValueError:
        pass

    # Check if student is already registered for this event (and not cancelled)
    existing = session.query(Registrations).filter(
        Registrations.event_id == event_id,
        Registrations.roll_no == roll_no,
        Registrations.cancelled_on.is_(None)
    ).first()

    if existing:
        session.close()
        return {"error": "Already registered for this event."}

    # Register student
    new_reg = Registrations(event_id=event_id, roll_no=roll_no)
    session.add(new_reg)
    event.seats_left -= 1

    session.commit()
    reg_id = new_reg.id
    session.close()

    return {
        "message": "Registration successful",
        "registration_id": reg_id
    }


# E6: GET STUDENT REGISTRATIONS
def get_student_registrations(roll_no):
    session = Session(engine)
    registrations = session.query(Registrations).filter(
        Registrations.roll_no == roll_no,
        Registrations.cancelled_on.is_(None)
    ).all()

    result = []
    for reg in registrations:
        event = session.get(Events, reg.event_id)
        if event is not None:
            result.append({
                "registration_id": reg.id,
                "event_id": event.id,
                "title": event.title,
                "event_date": event.event_date
            })

    session.close()
    return result


# E7: CANCEL REGISTRATION
def cancel_registration(registration_id):
    session = Session(engine)
    reg = session.get(Registrations, registration_id)
    if reg is None:
        session.close()
        return None

    # Check if already cancelled
    if reg.cancelled_on is not None:
        session.close()
        return {"error": "Registration already cancelled."}

    reg.cancelled_on = datetime.now()

    event = session.get(Events, reg.event_id)
    if event is not None:
        event.seats_left += 1

    session.commit()
    session.close()

    return {"message": "Registration cancelled successfully"}

    return {"message": "Registration cancelled successfully"}



