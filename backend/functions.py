from sqlalchemy import Integer,String,Column, create_engine, DateTime
from sqlalchemy.orm import Session, declarative_base
from datetime import datetime


DB_PATH = "./plants_orphange.db"
engine = create_engine(f"sqlite:///{DB_PATH}")
Base = declarative_base()


class Watering(Base):
    __tablename__ = "watering"
    id = Column(Integer, primary_key=True)
    plant_id = Column(Integer)
    roll_no = Column(String)
    watered_on = Column(DateTime , default=datetime.now())

Base.metadata.create_all(engine)