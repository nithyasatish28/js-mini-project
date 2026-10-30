from Backend.databaseorm import SessionLocal, Booking


def cancel_booking(booking_id):
    with SessionLocal() as db:
        booking = db.get(Booking, booking_id)

        if booking is None:
            return None

        if booking.cancelled == 1:
            return False

        booking.cancelled = 1
        db.commit()

        return True