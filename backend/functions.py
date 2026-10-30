from sqlalchemy import Column, Integer, String, create_engine, DateTime
from sqlalchemy.orm import Session, declarative_base
from datetime import datetime


DB_PATH = "hostel.db"

engine = create_engine(f"sqlite:///{DB_PATH}")

Base = declarative_base()


class Updates(Base):
    __tablename__ = "updates"
    id = Column(Integer, primary_key=True)
    complaint_id = Column(Integer)
    status = Column(String, default="open")
    note = Column(String)
    updated_on = Column(DateTime, default=datetime.now)


class Complaints(Base):
    __tablename__ = "complaints"
    id = Column(Integer, primary_key=True)
    roll_no = Column(String)
    room_no = Column(String)
    category = Column(String)
    description = Column(String)
    status = Column(String, default="open")
    created_on = Column(DateTime, default=datetime.now)
    resolved_on = Column(DateTime, nullable=True)


Base.metadata.create_all(engine)

CATEGORIES = ["electrical", "plumbing", "furniture", "cleaning", "internet"]


# E1
def get_all_complaints(status=None, category=None):
    session = Session(engine)
    complaints = session.query(Complaints).all()
    response = []

    for complaint in complaints:
        if status and complaint.status != status:
            continue
        if category and complaint.category != category:
            continue

        temp = {
            "id": complaint.id,
            "roll_no": complaint.roll_no,
            "room_no": complaint.room_no,
            "category": complaint.category,
            "description": complaint.description,
            "status": complaint.status,
            "created_on": complaint.created_on,
            "resolved_on": complaint.resolved_on
        }
        response.append(temp)

    session.close()
    return response


# E2
def get_complaint(id):
    session = Session(engine)
    complaint = session.get(Complaints, id)

    if complaint is None:
        session.close()
        return None

    response = {
        "id": complaint.id,
        "roll_no": complaint.roll_no,
        "room_no": complaint.room_no,
        "category": complaint.category,
        "description": complaint.description,
        "status": complaint.status,
        "created_on": complaint.created_on,
        "resolved_on": complaint.resolved_on
    }

    updates = session.query(Updates).filter(Updates.complaint_id == id).all()

    response["updates"] = []
    for update in updates:
        temp = {
            "status": update.status,
            "note": update.note,
            "updated_on": update.updated_on
        }
        response["updates"].append(temp)

    session.close()
    return response