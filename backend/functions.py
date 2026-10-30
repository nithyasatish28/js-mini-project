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



    