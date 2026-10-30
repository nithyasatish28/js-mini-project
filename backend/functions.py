from sqlalchemy import Integer, String, Column, DateTime, create_engine, inspect, ForeignKey
from sqlalchemy.orm import Session, declarative_base
from datetime import datetime

DB_PATH = "hostel.db"
engine = create_engine(f"sqlite:///{DB_PATH}")
Base = declarative_base()
print(inspect(engine).get_table_names())

class Complaint(Base):
    __tablename__ = "complaints"

    id = Column(Integer, primary_key=True)
    roll_no = Column(String)
    room_no = Column(String)
    category = Column(String)
    description = Column(String)
    status = Column(String)
    created_on = Column(DateTime, default=datetime.now)
    resolved_on = Column(DateTime, nullable=True)

class Update(Base):
    __tablename__ = "updates"
    id = Column(Integer, primary_key=True)
    
    status = Column(String)
    note = Column(String)
    updated_on = Column(DateTime, default=datetime.now)

Base.metadata.create_all(engine)

def get_all_complaints():
    session = Session(engine)
    complaints = session.query(Complaint).all()
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


def get_complaint(complaint_id):
    session = Session(engine)
    complaint = session.get(Complaint, complaint_id)
    if complaint is None:
        session.close()
        return None
    updates = session.query(Update).filter(Update.complaint_id == complaint_id).all()
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

    updates = []
    for update in updates:
        temp_update = {
            "id": update.id,
            "status": update.status,
            "note": update.note,
            "updated_on": update.updated_on
        }
        response["updates"].append(temp_update)
    session.close()
    return response



def get_complaint_by_status(status):
    pass