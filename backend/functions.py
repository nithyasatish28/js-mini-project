from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import Session, declarative_base

DB_PATH = "umbrellas.db"
engine = create_engine(f"sqlite:///{DB_PATH}")
Base = declarative_base()

class stations(Base):
    __tablename__ = "Stations"
    station_id = Column(String, primary_key=True)
    name = Column(String)
    location = Column(String)
    capacity = Column(Integer)
    umbrellas_available = Column(Integer)

class borrows(Base):
    __tablename__ = "Borrows"
    roll_no = Column(String, primary_key=True)
    from_station_id = Column(String, ForeignKey('Stations.station_id'))
    to_station_id = Column(String, ForeignKey('Stations.station_id'))
    borrowed_on = Column(DateTime, default=datetime.now)
    returned_on = Column(DateTime)

Base.metaengine.create_all(engine)









