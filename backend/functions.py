from sqlalchemy import Column, Integer, String, create_engine, DateTime
from sqlalchemy.orm import Session , declarative_base
from datetime import datetime


DB_PAth ="hostel_complaint_tracker.db"


engine=create_engine(f"sqlite:///{DB_PAth}")

Base=declarative_base()


class updates(Base):
    __tablename__="updates"
    id=Column(Integer,primary_key=True)
    complaint_id=Column(String)
    status=Column(String)
    note=Column(String,nullable=True)
    updated_on=Column(DateTime,default=datetime.now)

class complaints(Base):
    __tablename__="complaints"
    id=Column(Integer ,primary_key=True)
    rollno = Column(String)
    room_no = Column(Integer)
    category = Column(String)
    description = Column(String)
    status = Column(String)
    created_on = Column(DateTime,default=datetime.now)
    resolved_on = Column(DateTime, nullable=True)

Base.metadata.create_all(engine) 

def get_complaints(status=None,category=None):
    session=Session(engine)
    query = session.query(complaints)
    if status:
        query = query.filter(complaints.status==status)
    if category:
        query=query.filter(complaints.category==category)
    respone=[]
    for complaint in query:
        temp = {
            "id" : complaint.id,
            "roll_no" : complaint.rollno,
            "room_no" : complaint.room_no,
            "category" : complaint.category,
            "description" : complaint.description,
            "status" : complaint.status,
            "created_on" : complaint.created_on,
            "resolved_on" : complaint.resolved_on
        }
        respone.append(temp)
    session.close()
    if respone == []:
        return None
    return respone

def get_one_complaint(id:int):
    session = Session(engine)
    query = session.query(complaints).filter(complaints.id == id).first()
    if not query:
            return None
    query2 = session.query(updates).filter(updates.complaint_id == id).all()
    response =[]
    temp1 = {
        "id" : query.id,
        "roll_no" : query.rollno,
        "room_no" : query.room_no,
        "category" : query.category,
        "description" : query.description,
        "status" : query.status,
        "created_on" : query.created_on,
        "resolved_on" : query.resolved_on
    }
    response.append(temp1)
    for update in query2:
        temp = {
            "id" : update.id,
            "status" : update.status,
            "note" : update.note,
            "updated_on" : update.updated_on
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
        "id" : complaint.id,
        "roll_no" : complaint.rollno,
        "room_no" : complaint.room_no,
        "category" : complaint.category,
        "description" : complaint.description,
        "status" : complaint.status,
        "created_on" : complaint.created_on,
        "resolved_on" : complaint.resolved_on
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

<<<<<<< HEAD
def get_complaints_bystatus
=======

def get_students_complaints_byrollno(rollno):
    session = Session(engine)
    query = session.query(complaints).filter(complaints.rollno==rollno).all()
    response=[]
    for complaint in query:
        temp = {
            "id" : complaint.id,
            "roll_no" : complaint.rollno,
            "room_no" : complaint.room_no,
            "category" : complaint.category,
            "description" : complaint.description,
            "status" : complaint.status,
            "created_on" : complaint.created_on,
            "resolved_on" : complaint.resolved_on
        }
        response.append(temp)
    session.close()
    if response==[]:
        return None
    return response
>>>>>>> 9c362af46c6f375e84790b2ea85c8ce614f4eb4d
