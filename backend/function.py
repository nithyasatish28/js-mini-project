from sqlalchemy import Integer, String, Column, create_engine, DateTime, ForeignKey
from sqlalchemy.orm import Session, declarative_base
from datetime import datetime, date

DB_PATH = "garden.db"
engine = create_engine(f"sqlite:///{DB_PATH}")
Base = declarative_base()


class Plants(Base):
    __tablename__ = "plants"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    type = Column(String)
    location = Column(String, nullable=True)
    water_every_days = Column(Integer)
    adopted_by = Column(String, nullable=True)


class Waterings(Base):
    __tablename__ = "waterings"

    id = Column(Integer, primary_key=True)
    roll_no = Column(String)
    plant_id = Column(Integer, ForeignKey("plants.id"))
    watered_on = Column(DateTime, default=datetime.now)


Base.metadata.create_all(engine)

