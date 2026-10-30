from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, create_engine
from sqlalchemy.orm import Session, declarative_base

DB_PATH = "complaints.db"
engine = create_engine(f"sqlite:///{DB_PATH}")
Base = declarative_base()


class Complaints(Base):
    __tablename__ = "Complaints"

    id = Column(Integer, primary_key=True)
    roll_no = Column(Integer)
    room_no = Column(String)
    catagory = Column(String)
    description = Column(String)
    status = Column(String)
    created_on = Column(DateTime, default=datetime.now)
    resolved_on = Column(DateTime, nullable=True)


Base.metadata.create_all(engine)


def _to_datetime(value):
    if value is None:
        return None
    if isinstance(value, datetime):
        return value
    return datetime.fromisoformat(str(value))


def _Complaints_to_dict(item):
    return {
        "id": item.id,
        "roll_no": item.roll_no,
        "room_no": item.room_no,
        "catagory": item.catagory,
        "description": item.description,
        "status": item.status,
        "created_on": item.created_on,
        "resolved_on": item.resolved_on,
    }


def add_complaint(roll_no, room_no, catagory=None, description="", status="active", created_on=None, resolved_on=None, location=None):
    created_on = _to_datetime(created_on) if created_on is not None else datetime.now()
    resolved_on = _to_datetime(resolved_on)

    with Session(engine) as session:
        item = Complaints(
            roll_no=roll_no,
            room_no=room_no,
            catagory=catagory,
            description=description,
            status=status,
            created_on=created_on,
            resolved_on=resolved_on,
        )
        session.add(item)
        session.commit()
        session.refresh(item)
        return _Complaints_to_dict(item)


def get_all_Complaints():
    with Session(engine) as session:
        items = session.query(Complaints).all()
        return [_Complaints_to_dict(item) for item in items]


def get_Complaints(id_):
    with Session(engine) as session:
        item = session.get(Complaints, id_)
        return _Complaints_to_dict(item) if item is not None else None


def update_complaint(complaint_id, **kwargs):
    with Session(engine) as session:
        item = session.get(Complaints, complaint_id)
        if item is None:
            return None

        for key, value in kwargs.items():
            if hasattr(item, key):
                if key in {"created_on", "resolved_on"}:
                    value = _to_datetime(value)
                setattr(item, key, value)

        session.commit()
        session.refresh(item)
        return _Complaints_to_dict(item)


def delete_complaint(complaint_id):
    with Session(engine) as session:
        item = session.get(Complaints, complaint_id)
        if item is None:
            return False

        session.delete(item)
        session.commit()
        return True

