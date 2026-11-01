from sqlalchemy import Integer, String, Column, DateTime, create_engine, inspect, ForeignKey
from sqlalchemy.orm import Session, declarative_base
from datetime import datetime

DB_PATH = "hostel.db"
engine = create_engine(f"sqlite:///{DB_PATH}")
Base = declarative_base()
print(inspect(engine).get_table_names())

class Complaint(Base):
    __tablename__ = "complaints"
    id = Column(Integer, primary_key=True)
    roll_no = Column(Integer)
    room_no = Column(Integer)
    category = Column(String)
    description = Column(String)
    status = Column(String)
    created_on = Column(DateTime, default=datetime.now)
    resolved_on = Column(DateTime, nullable=True)

class Update(Base):
    __tablename__ = "updates"
    id = Column(Integer, primary_key=True)
    complaint_id = Column(Integer, ForeignKey("complaints.id"))
    status = Column(String)
    note = Column(String)
    updated_on = Column(DateTime, default=datetime.now)

Base.metadata.create_all(engine)

def get_all_complaints():
    session = Session(engine)
    complaints = session.query(Complaint).all()
    response = []
    for complaint in complaints:
        temp_complaint = {
            "id": complaint.id,
            "roll_no": complaint.roll_no,
            "room_no": complaint.room_no,
            "category": complaint.category,
            "description": complaint.description,
            "status": complaint.status,
            "created_on": complaint.created_on,
            "resolved_on": complaint.resolved_on
        }
        response.append(temp_complaint)
    session.close()
    return response


def get_complaint(complaint_id):
    session = Session(engine)
    complaint = session.get(Complaint, complaint_id)
    if complaint is None:
        session.close()
        return None
    updates = session.query(Update).filter(Update.complaint_id == complaint_id).all()

    response = {
        "id": complaint.id,
        "roll_no": complaint.roll_no,
        "room_no": complaint.room_no,
        "category": complaint.category,
        "description": complaint.description,
        "status": complaint.status,
        "created_on": complaint.created_on,
        "resolved_on": complaint.resolved_on,
        # "updates": []
    }
    updates = []
    for update in updates:
        temp_update = {
            "id": update.id,
            "status": update.status,
            "note": update.note,
            "updated_on": update.updated_on
        }

        response["updates"].append(temp_update)
    session.close()
    return response

def add_complaint(roll_no, room_no, category, description):
    session = Session(engine)
    if roll_no <= 0 or room_no <= 0:
        session.close()
        return None
    existing_complaint = session.query(Complaint).filter(
    Complaint.roll_no == roll_no,
    Complaint.category == category,
    Complaint.status != "resolved"
).first()
    if existing_complaint is not None:
        session.close()
        return False
    complaint = Complaint(
        roll_no=roll_no,
        room_no=room_no,
        category=category,
        description=description,
        status="open"
    )
    session.add(complaint)
    session.commit()
    session.refresh(complaint)
    response = {
        "id": complaint.id,
        "roll_no": complaint.roll_no,
        "room_no": complaint.room_no,
        "category": complaint.category,
        "description": complaint.description,
        "status": complaint.status,
        "created_on": complaint.created_on
    }
    session.close()
    return response

def update_complaint(complaint_id, status, note):
    session = Session(engine)
    complaint = session.get(Complaint, complaint_id)
    if complaint is None:
        session.close()
        return None
    if complaint.status == "resolved":
        session.close()
        return False
    if status != "in_progress" and status != "resolved":
        session.close()
        return False
    if complaint.status == "open" and status != "in_progress":
        session.close()
        return False
    if complaint.status == "in_progress" and status != "resolved":
        session.close()
        return False
    complaint.status = status
    if status == "resolved":
        complaint.resolved_on = datetime.now()
    update = Update(
        complaint_id=complaint_id,
        status=status,
        note=note
    )
    session.add(update)
    session.commit()
    response = {
        "id": complaint.id,
        "status": complaint.status,
        "note": note
    }
    session.close()
    return response

def get_student_complaints(roll_no):
    session = Session(engine)
    complaints = session.query(Complaint).filter(Complaint.roll_no == roll_no).all()
    response = []
    for complaint in complaints:
        temp_complaint = {
            "id": complaint.id,
            "roll_no": complaint.roll_no,
            "room_no": complaint.room_no,
            "category": complaint.category,
            "description": complaint.description,
            "status": complaint.status,
            "created_on": complaint.created_on,
            "resolved_on": complaint.resolved_on
        }
        response.append(temp_complaint)
    session.close()
    return response

# def get_student_complaints(roll_no):
#     session = Session(engine)
#     complaints = session.query(Complaint).filter(
#         Complaint.roll_no == roll_no
#     ).all()
#     session.close()
#     if not complaints:
#         return {"message": "No complaints found for this roll number"}
#     return complaints


def delete_complaint(complaint_id):
    session = Session(engine)
    complaint = session.get(Complaint, complaint_id)
    if complaint is None:
        session.close()
        return None
    if complaint.status != "open":
        session.close()
        return False
    session.query(Update).filter(Update.complaint_id == complaint_id).delete()
    session.delete(complaint)
    session.commit()
    session.close()
    return True


def get_complaint_counts():
    session = Session(engine)
    response = {
        "open": 0,
        "in_progress": 0,
        "resolved": 0
    }
    complaints = session.query(Complaint).all()
    for complaint in complaints:
        response[complaint.status] += 1
    session.close()
    return response

