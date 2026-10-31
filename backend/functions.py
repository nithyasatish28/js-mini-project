from sqlalchemy import Column, Integer, String, create_engine, DateTime, func
from sqlalchemy.orm import Session, declarative_base
from datetime import datetime

DB_PATH = "hostel_complaint_tracker.db"

engine = create_engine(f"sqlite:///{DB_PATH}")

Base = declarative_base()

class updates(Base):
    __tablename__ = "updates"
    id = Column(Integer, primary_key=True)
    complaint_id = Column(String)
    status = Column(String)
    note = Column(String, nullable=True)
    updated_on = Column(DateTime, default=datetime.now)

class complaints(Base):
    __tablename__ = "complaints"
    id = Column(Integer, primary_key=True)
    rollno = Column(String)
    room_no = Column(Integer)
    category = Column(String)
    description = Column(String)
    status = Column(String)
    created_on = Column(DateTime, default=datetime.now)
    resolved_on = Column(DateTime, nullable=True)

Base.metadata.create_all(engine) 


def get_complaints(status=None, category=None):
    session = Session(engine)
    query = session.query(complaints)
    if status:
        query = query.filter(complaints.status == status)
    if category:
        query = query.filter(complaints.category == category)
    response = []
    for complaint in query:
        temp = {
            "id": complaint.id,
            "roll_no": complaint.rollno,
            "room_no": complaint.room_no,
            "category": complaint.category,
            "description": complaint.description,
            "status": complaint.status,
            "created_on": complaint.created_on,
            "resolved_on": complaint.resolved_on
        }
        response.append(temp)
    session.close()
    if response == []:
        return None
    return response


def get_one_complaint(id: int):
    session = Session(engine)
    query = session.query(complaints).filter(complaints.id == id).first()
    if not query:
        session.close()
        return None
        
    query2 = session.query(updates).filter(updates.complaint_id == str(id)).all()
    response = []
    temp1 = {
        "id": query.id,
        "roll_no": query.rollno,
        "room_no": query.room_no,
        "category": query.category,
        "description": query.description,
        "status": query.status,
        "created_on": query.created_on,
        "resolved_on": query.resolved_on
    }
    response.append(temp1)
    
    for update in query2:
        temp = {
            "id": update.id,
            "status": update.status,
            "note": update.note,
            "updated_on": update.updated_on
        }
        response.append(temp)
    session.close()
    return response


def create_complaint(rollno, roomno, category, description):
    session = Session(engine)
    complaint = complaints(rollno=rollno, room_no=roomno, category=category, description=description, status="open")    
    session.add(complaint)
    session.commit()
    session.refresh(complaint)
    
    temp = {
        "id": complaint.id,
        "roll_no": complaint.rollno,
        "room_no": complaint.room_no,
        "category": complaint.category,
        "description": complaint.description,
        "status": complaint.status,
        "created_on": complaint.created_on,
        "resolved_on": complaint.resolved_on
    }
    session.close()
    return temp


def update_complaint_status(complaint_id, new_status, note):
    session = Session(engine)
    complaint = session.query(complaints).filter(complaints.id == complaint_id).first()
    
    if not complaint:
        session.close()
        return {"error": "Complaint not found"}
        
    complaint.status = new_status
    if new_status.lower() == "resolved":
        complaint.resolved_on = datetime.now()
        
    status_update = updates(complaint_id=str(complaint_id), status=new_status, note=note)
    session.add(status_update)
    session.commit()
    
    temp = {
        "complaint_id": complaint.id,
        "new_status": complaint.status,
        "resolved_on": complaint.resolved_on,
        "message": "Status updated and note added successfully"
    }
    session.close()
    return temp


def get_students_complaints_byrollno(rollno):
    session = Session(engine)
    query = session.query(complaints).filter(complaints.rollno == rollno).all()
    response = []
    for complaint in query:
        temp = {
            "id": complaint.id,
            "roll_no": complaint.rollno,
            "room_no": complaint.room_no,
            "category": complaint.category,
            "description": complaint.description,
            "status": complaint.status,
            "created_on": complaint.created_on,
            "resolved_on": complaint.resolved_on
        }
        response.append(temp)
    session.close()
    if response == []:
        return None
    return response


def delete_complaint(complaint_id: int):
    session = Session(engine)
    complaint = session.query(complaints).filter(complaints.id == complaint_id).first()
    
    if not complaint:
        session.close()
        return {"error": "Complaint not found"}
     
    session.query(updates).filter(updates.complaint_id == str(complaint_id)).delete()
    
   
    session.delete(complaint)
    session.commit()
    session.close()
    return {"message": "Complaint and its updates deleted successfully"}


def get_complaint_status_counts():
    session = Session(engine)
    results = session.query(complaints.status, func.count(complaints.id)).group_by(complaints.status).all()
    session.close()
    return {status: count for status, count in results}

