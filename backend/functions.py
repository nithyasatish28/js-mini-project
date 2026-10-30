from sqlalchemy import Integer, String, Column, DateTime, create_engine
from sqlalchemy.orm import Session, declarative_base
from datetime import datetime

DB_PATH = "hostel.db"
engine = create_engine(f"sqlite:///{DB_PATH}")
Base = declarative_base()

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
    complaint_id = Column(Integer)
    status = Column(String)
    note = Column(String)
    updated_on = Column(DateTime, default=datetime.now)

Base.metadata.create_all(engine)

