from sqlalchemy import Integer, String, Column, create_engine, DateTime
from sqlalchemy.orm import Session, declarative_base
from datetime import datetime

DB_PATH = "plant.db"
engine = create_engine(f"sqlite:///{DB_PATH}")
Base = declarative_base()



class Items(Base):
    __tablename__ = "plants"
    id = Column(Integer, primary_key=True)
    name =  Column(String)
    type = Column(String)
    
    location = Column(String, nullable=True)
    
    water_every_days = Column(Integer)
    adopted_by = Column(String, nullable=True)

Base.metadata.create_all(engine)


class Items(Base):
    __tablename__ = "waterings"
    id = Column(Integer, primary_key=True)
    roll_no =  Column(Integer)
    plant_id = Column(Integer, foreign_key="plants.id")
    
    watered_on = Column(Integer, default=datetime.now().timestamp())
    

Base.metadata.create_all(engine)



