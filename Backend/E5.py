from enum import Enum

from Backend.databaseorm import Booking, Equipment, SessionLocal


class BookingResult(Enum):
    BOOKED = "booked"
    EQUIPMENT_NOT_FOUND = "equipment_not_found"
    EQUIPMENT_OUT_OF_SERVICE = "equipment_out_of_service"
    EQUIPMENT_ALREADY_BOOKED = "equipment_already_booked"
    STUDENT_BOOKING_LIMIT_REACHED = "student_booking_limit_reached"


def book_equipment(equipment_id: int, roll_no: str, booking_date: str) -> BookingResult:
    with SessionLocal() as session:
        equipment = session.query(Equipment).filter(Equipment.id == equipment_id).first()
        if equipment is None:
            return BookingResult.EQUIPMENT_NOT_FOUND
        if not equipment.in_service:
            return BookingResult.EQUIPMENT_OUT_OF_SERVICE

        existing_booking = session.query(Booking).filter(
            Booking.equipment_id == equipment_id,
            Booking.booking_date == booking_date,
            Booking.cancelled == 0,
        ).first()
        if existing_booking is not None:
            return BookingResult.EQUIPMENT_ALREADY_BOOKED

        student_bookings = session.query(Booking).filter(
            Booking.roll_no == roll_no,
            Booking.booking_date == booking_date,
            Booking.cancelled == 0,
        ).count()
        if student_bookings >= 2:
            return BookingResult.STUDENT_BOOKING_LIMIT_REACHED

        booking = Booking(
            equipment_id=equipment_id,
            roll_no=roll_no,
            booking_date=booking_date,
        )
        session.add(booking)
        session.commit()
        return BookingResult.BOOKED
    
    
    
    
    
