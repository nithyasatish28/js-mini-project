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
    return respone



    
