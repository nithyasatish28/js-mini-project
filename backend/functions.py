from sqlalchemy import Column, Integer, String, create_engine, DateTime
from sqlalchemy.orm import Session , declarative_base
from datetime import datetime


DB_PAth ="hostel_complaint_tracker.db"


engine=create_engine(f"sqlite:///{DB_PAth}")

Base=declarative_base()
Base.metadata.create_all(engine) 

class Updates(Base):
    __tablename__="updates"
    id=Column(Integer,primary_key=True)
    complaint_id=Column(String)
    status=Column(String)
    note=Column(String,nullable=True)
    updated_on=Column(DateTime,default=datetime.now)

class Complaints(Base):
    __tablename__="complaints"
    id=Column(Integer ,primary_key=True)
    rollno = Column(String)
    room_no = Column(Integer)
    category = Column(String)
    description = Column(String)
    status = Column(String)
    created_on = Column(DateTime,default=datetime.now)
    resolved_on = Column(DateTime, nullable=True)

    
