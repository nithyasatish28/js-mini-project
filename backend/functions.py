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
    __tablename__="complaints"
    id=Column(Integer,primary_key=True)
    roll_no=Column(String)
    room_no=Column(String)
    category=Column(String)
    description=Column(String)
    status=Column(String,default="open")
    created_on=Column(DateTime,default=datetime.now)
    resolved_on=Column(DateTime,nullable=True)

Base.metadata.create_all(engine)

CATEGORIES = ["electrical", "plumbing", "furniture", "cleaning", "internet"]

NEXT_STATUS = {"open": "in_progress", "in_progress": "resolved"}


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

#3
def create_complaint(rollno, roomno, category, description):
    session = Session(engine)

    complaint = Complaints(
        roll_no=rollno,
        room_no=roomno,
        category=category,
        description=description,
        status="open"
    )

    session.add(complaint)
    session.commit()

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

    session.close()
    return temp

#4
def update_complaint(id, note):
    session = Session(engine)
    complaint = session.get(Complaints, id)

    if complaint is None or complaint.status not in NEXT_STATUS:
        session.close()
        return None

    new_status = NEXT_STATUS[complaint.status]
    complaint.status = new_status

    if new_status == "resolved":
        complaint.resolved_on = datetime.now()

    update = Updates(
        complaint_id=id,
        status=new_status,
        note=note
    )
    session.add(update)
    session.commit()

    temp = {
        "id": complaint.id,
        "status": complaint.status,
        "note": update.note,
        "updated_on": update.updated_on
    }

    session.close()
    return temp

#5
def fetch_student_complaint(roll_no):
    session = Session(engine)

    complaints = session.query(Complaints).filter(
        Complaints.roll_no == roll_no
    ).all()

    response = []

    for complaint in complaints:
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

#6
def remove_complaint(id):
    session = Session(engine)
    complaint = session.get(Complaints, id)

    if complaint is None or complaint.status != "open":
        session.close()
        return False

    session.query(Updates).filter(
        Updates.complaint_id == id
    ).delete()

    session.delete(complaint)
    session.commit()
    session.close()

    return True

#7
def get_status_counts():
    session = Session(engine)

    temp = {
        "open": session.query(Complaints).filter(
            Complaints.status == "open"
        ).count(),

        "in_progress": session.query(Complaints).filter(
            Complaints.status == "in_progress"
        ).count(),

        "resolved": session.query(Complaints).filter(
            Complaints.status == "resolved"
        ).count()
    }

    session.close()
    return temp
