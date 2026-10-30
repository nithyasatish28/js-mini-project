from sqlalchemy import String, Integer, Column, create_engine, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, Session 
from datetime import datetime

db_path = "hostel.db"
engine = create_engine(f"sqlite:///{db_path}")
Base = declarative_base() 

Categories = ["electrical", "plumbing", "furniture", "cleaning", "internet"]
Statuses = ["open", "in_progress", "resolved"]

class Complaints(Base):
    __tablename__ = "Complaints"
    id = Column(Integer, primary_key=True, autoincrement=True)
    roll_no = Column(String)
    room_no = Column(String)
    category = Column(String)
    description = Column(String(500))
    status = Column(String)
    created_on = Column(DateTime, default=datetime.now)
    resolved_on = Column(DateTime)


class Updates(Base):
    __tablename__ = "Updates"
    id = Column(Integer, primary_key=True, autoincrement=True)
    complaint_id = Column(Integer, ForeignKey("Complaints.id"))
    status = Column(String)
    note = Column(String(1000))
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
        "created_on": complaint.created_on

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
        updates = session.query(Updates).filter(Updates.complaint_id == complaint_id).all()
        for update in updates:
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

