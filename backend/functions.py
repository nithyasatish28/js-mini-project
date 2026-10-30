from sqlalchemy import Column, Integer, String, create_engine, DateTime
from sqlalchemy.orm import Session , declarative_base
from datetime import datetime


DB_PAth ="hostel_complaint_tracker.db"


engine=create_engine(f"sqlite:///{DB_PAth}")

Base=declarative_base()


class Updates(Base):
    __tablename__="updates"
    id=Column(String,primary_key=True)
    complaint_id=Column(String)
    status=Column(String)
    note=Column(String,nullable=True)
    updated_on=Column(DateTime,default=datetime.now)

Base.metadata.create_all(engine) 

    
