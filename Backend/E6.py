from datetime import date
from Backend.databaseorm import SessionLocal, Booking, Equipment


def get_student_bookings(roll_no):
    with SessionLocal() as db:
        today = str(date.today())

        bookings = db.query(Booking).filter(
            Booking.roll_no == roll_no,
            Booking.cancelled == 0,
            Booking.booking_date >= today
        ).all()

        result = []

        for booking in bookings:
            equipment = db.get(Equipment, booking.equipment_id)

            result.append({
                "id": booking.id,
                "equipment_id": booking.equipment_id,
                "equipment_name": equipment.name,
                "roll_no": booking.roll_no,
                "booking_date": booking.booking_date
            })

        return result