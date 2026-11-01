from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, String, DateTime  # type: ignore
from sqlalchemy.orm import declarative_base, Session  # type: ignore

DB_PATH = "lost_found.db"
engine = create_engine(f"sqlite:///{DB_PATH}", echo=True)
Base = declarative_base()


class Items(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    posted_at = Column(DateTime, default=datetime.now)
    location = Column(String)
    status = Column(String)
    contact = Column(String)
    resolved_at = Column(DateTime, nullable=True)


Base.metadata.create_all(engine)


def _item_to_dict(item):
    return {
        "id": item.id,
        "name": item.name,
        "description": item.description,
        "posted_at": item.posted_at,
        "location": item.location,
        "status": item.status,
        "contact": item.contact,
        "resolved_at": item.resolved_at,
    }


def add_lost_item(name, description, contact, location=None):
    with Session(engine) as session:
        item = Items(
            name=name,
            description=description,
            contact=contact,
            location=location,
            status="active",
        )
        session.add(item)
        session.commit()
        session.refresh(item)
        return _item_to_dict(item)


def get_all_items():
    with Session(engine) as session:
        items = session.query(Items).all()
        return [_item_to_dict(item) for item in items]


def get_item(id):
    with Session(engine) as session:
        item = session.get(Items, id)
        return _item_to_dict(item) if item is not None else None
