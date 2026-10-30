from sqlalchemy import String, Integer, Column, create_engine, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, Session 
from datetime import datetime

db_path = "hostel.db"
engine = create_engine(f"sqlite:///{db_path}")
Base = declarative_base() 

Categories = ["electrical", "plumbing", "furniture", "cleaning", "internet"]
Statuses = ["open", "in_progress", "resolved"]
Next_status = {"open": "in_progress", "in_progress": "resolved"}


class Complaints(Base):
    __tablename__ = "Complaints"
    id = Column(Integer, primary_key=True, autoincrement=True)
    roll_no = Column(String)
    room_no = Column(String)
    category = Column(String)
    description = Column(String(500))
    status = Column(String, default="open")
    created_on = Column(DateTime, default=datetime.now)
    resolved_on = Column(DateTime)


class Updates(Base):
    __tablename__ = "Updates"
    id = Column(Integer, primary_key=True, autoincrement=True)
    complaint_id = Column(Integer, ForeignKey("Complaints.id"))
    status = Column(String)
    note = Column(String(500))
    updated_on = Column(DateTime, default=datetime.now)

Base.metadata.create_all(engine)


def get_all_complaints():
    session = Session(engine)
    complaints = session.query(Complaints).all()
    response = []
    for complaint in complaints:
        temp_complaint = {
        "id": complaint.id,
        "roll_no": complaint.roll_no,
        "room_no": complaint.room_no,
        "category": complaint.category,
        "description": complaint.description,
        "status": complaint.status,
        "created_on": complaint.created_on,
        "resolved_on": complaint.resolved_on

    }
        response.append(temp_complaint)
    session.close()
    return response

def get_complaint_by_id(complaint_id):
    session = Session(engine)
    complaint = session.query(Complaints).filter(Complaints.id == complaint_id).first()
    if complaint:
        response = {
            "id": complaint.id,
            "roll_no": complaint.roll_no,
            "room_no": complaint.room_no,
            "category": complaint.category,
            "description": complaint.description,
            "status": complaint.status,
            "created_on": complaint.created_on,
            "resolved_on": complaint.resolved_on,
            "updates": []
        }
        all_updates = session.query(Updates).all()
        for update in all_updates:
            if update.complaint_id == complaint_id:
                temp_update = {
                    "id": update.id,
                    "status": update.status,
                    "note": update.note,
                    "updated_on": update.updated_on
                }
                response["updates"].append(temp_update)
    else:
        response = None
    session.close()
    return response

def add_new_complaint(roll_no, room_no, category, description):
    session = Session(engine)
    complaint = Complaints(roll_no=roll_no, room_no=room_no,category=category, description=description, status="open")
    session.add(complaint)
    session.commit()
    response = {
        "id": complaint.id,
        "roll_no": complaint.roll_no,
        "room_no": complaint.room_no,
        "category": complaint.category,
        "description": complaint.description,
        "status": complaint.status,
        "created_on": complaint.created_on
    }
    session.close()
    return response

def update_complaint(complaint_id, note):
    session = Session(engine)
    complaint = session.query(Complaints).filter(Complaints.id == complaint_id).first()
    complaint.status = Next_status[complaint.status]
    if complaint.status == "resolved":
        complaint.resolved_on = datetime.now()
    update = Updates(complaint_id=complaint_id, status=complaint.status, note=note)
    session.add(update)
    session.commit()
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
    session.close()
    return response


def fetch_student_complaint(roll_no):
    session = Session(engine)
    complaints = session.query(Complaints).filter(Complaints.roll_no == roll_no).all()
    response = []
    for complaint in complaints:
        temp_complaint = {
            "id": complaint.id,
            "roll_no": complaint.roll_no,
            "room_no": complaint.room_no,
            "category": complaint.category,
            "description": complaint.description,
            "status": complaint.status,
            "created_on": complaint.created_on,
            "resolved_on": complaint.resolved_on
        }
        response.append(temp_complaint)
    session.close()
    return response


def remove_complaint(complaint_id):
    session = Session(engine)
    all_updates = session.query(Updates).all()
    for update in all_updates:
        if update.complaint_id == complaint_id:
            session.delete(update)
    complaint = session.query(Complaints).filter(Complaints.id == complaint_id).first()
    session.delete(complaint)
    session.commit()
    session.close()

def filter_complaint(status = None, category = None):
    session = Session(engine)
    if status is not None and category is not None:
        complaints = session.query(Complaints).filter(Complaints.status == status, Complaints.category == category).all()
    elif status is not None:
        complaints = session.query(Complaints).filter(Complaints.status == status).all()
    elif category is not None:
        complaints = session.query(Complaints).filter(Complaints.category == category).all()
    else:
        complaints = session.query(Complaints).all()
    response = []
    for complaint in complaints:
        temp_complaint = {
            "id": complaint.id,
            "roll_no": complaint.roll_no,
            "room_no": complaint.room_no,
            "category": complaint.category,
            "description": complaint.description,
            "status": complaint.status,
            "created_on": complaint.created_on,
            "resolved_on": complaint.resolved_on
        }
        response.append(temp_complaint)
    session.close()
    return response
