from sqlalchemy import Integer, String, Column, create_engine,DateTime 
from sqlalchemy.orm import Session, declarative_base
from datetime import datetime
from database import Base, engine

DB_PATH ="events.db"
engine =create_engine(f"sqlite:///{DB_PATH}")
Base = declarative_base()


class Events(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    club = Column(String)
    category = Column(String)
    event_date = Column(Integer)
    total_seats = Column(Integer)
    seats_left = Column(Integer)
