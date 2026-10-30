from sqlalchemy import Integer, String, Column, create_engine, DateTime, ForeignKey
from sqlalchemy.orm import Session, declarative_base
from datetime import datetime


DB_PATH = "./plants_orphange.db"
engine = create_engine(f"sqlite:///{DB_PATH}")
Base = declarative_base()

class Plants(Base):
    __tablename__ = "plants"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    type = Column(String)
    location = Column(String)
    water_every_days = Column(Integer)
    adopted_by = Column(String, nullable=True)


class Watering(Base):
    __tablename__ = "waterings"
    id = Column(Integer, primary_key=True)
    plant_id = Column(Integer, ForeignKey("plants.id"))
    roll_no = Column(String)
    watered_on = Column(DateTime , default=datetime.now())

Base.metadata.create_all(engine)