from Backend.databaseorm import Booking, Equipment, SessionLocal


def book_equipment(equipment_id, roll_no, booking_date):
    with SessionLocal() as session:
        equipment = session.query(Equipment).filter(Equipment.id == equipment_id).first()
        if not equipment or not equipment.in_service:
            return False

        booking = Booking(
            equipment_id=equipment_id,
            roll_no=roll_no,
            booking_date=booking_date,
        )
        session.add(booking)
        session.commit()
        return True
    
    
    
    
    
