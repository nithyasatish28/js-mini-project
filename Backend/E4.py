#E4	Mark an item in service or out of service. so i should be able to change the status like attribute called in service or out of service
from Backend.databaseorm import SessionLocal, Equipment

def mark_equipment_status(equipment_id: int, in_service: bool) -> bool:
    session = SessionLocal()
    try:
        equipment = session.query(Equipment).filter(Equipment.id == equipment_id).first()
        if equipment is None:
            return False

        equipment.in_service = in_service
        session.commit()
        return True
    finally:
        session.close()