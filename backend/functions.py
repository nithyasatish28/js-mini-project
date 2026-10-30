from sqlalchemy import String , Integer , Column ,DATE, create_engine
from sqlalchemy.orm import Session , declarative_base
from datetime import datetime

DB_PATH ="hostel_complaint_tracker.db"
engine = create_engine(f"sqlite:///{DB_PATH}")
Base = declarative_base()

class updates(Base):