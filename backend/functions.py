from datetime import datetime
from pathlib import Path

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import Session, declarative_base
from sqlalchemy.types import TypeDecorator

DB_PATH = Path(__file__).with_name("complaints.db")
engine = create_engine(f"sqlite:///{DB_PATH.as_posix()}")
Base = declarative_base()


class FlexibleDateTime(TypeDecorator):
    impl = String
    cache_ok = True

    def process_bind_param(self, value, dialect):
        return value.isoformat() if value is not None else None

    def process_result_value(self, value, dialect):
        if value is None or isinstance(value, datetime):
            return value
        return datetime.fromisoformat(value.replace("Z", "+00:00"))


class Complaints(Base):
    __tablename__ = "Complaints"

    id = Column(Integer, primary_key=True)
    roll_no = Column(Integer)
    room_no = Column(String)
    catagory = Column(String)
    description = Column(String)
    status = Column(String)
    created_on = Column(FlexibleDateTime, default=datetime.now)
    resolved_on = Column(FlexibleDateTime, nullable=True)


Base.metadata.create_all(engine)


def _complaint_to_dict(complaint):
    return {
        "id": complaint.id,
        "roll_no": complaint.roll_no,
        "room_no": complaint.room_no,
        "catagory": complaint.catagory,
        "description": complaint.description,
        "status": complaint.status,
        "created_on": complaint.created_on,
        "resolved_on": complaint.resolved_on,
    }


def add_complaint(roll_no, room_no, catagory=None, description="", status="active"):
    with Session(engine) as session:
        complaint = Complaints(
            roll_no=roll_no,
            room_no=room_no,
            catagory=catagory,
            description=description,
            status=status,
            resolved_on=datetime.now() if status.lower() in {"resolved", "closed"} else None,
        )
        session.add(complaint)
        session.commit()
        session.refresh(complaint)
        return _complaint_to_dict(complaint)


def get_all_complaints():
    with Session(engine) as session:
        complaints = session.query(Complaints).order_by(Complaints.created_on.desc()).all()
        return [_complaint_to_dict(complaint) for complaint in complaints]


def get_complaint(id):
    with Session(engine) as session:
        complaint = session.get(Complaints, id)
        return _complaint_to_dict(complaint) if complaint is not None else None


def get_complaints_by_status(status):
    with Session(engine) as session:
        complaints = (
            session.query(Complaints)
            .filter(Complaints.status == status)
            .order_by(Complaints.created_on.desc())
            .all()
        )
        return [_complaint_to_dict(complaint) for complaint in complaints]


def update_complaint(id, **kwargs):
    with Session(engine) as session:
        complaint = session.get(Complaints, id)
        if complaint is None:
            return None

        for key, value in kwargs.items():
            setattr(complaint, key, value)
            if key == "status":
                complaint.resolved_on = datetime.now() if value.lower() in {"resolved", "closed"} else None

        session.commit()
        session.refresh(complaint)
        return _complaint_to_dict(complaint)


def delete_complaint(id):
    with Session(engine) as session:
        complaint = session.get(Complaints, id)
        if complaint is None:
            return False

        session.delete(complaint)
        session.commit()
        return True


def resolve_complaint(id):
    with Session(engine) as session:
        complaint = session.get(Complaints, id)
        if complaint is None:
            return None

        complaint.status = "resolved"
        complaint.resolved_on = datetime.now()
        session.commit()
        session.refresh(complaint)
        return _complaint_to_dict(complaint)
