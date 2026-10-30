from sqlalchemy import Integer,String,Column, create_engine, DateTime
from sqlalchemy.orm import Session, declarative_base
from datetime import datetime


DB_PATH = "./plants_orphange.db"
engine = create_engine(f"sqlite:///{DB_PATH}")
Base = declarative_base()