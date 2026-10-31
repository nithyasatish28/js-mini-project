import { useState } from "react";

function MyBookings({ bookings, onShow, onCancel }) {

  const [rollNo, setRollNo] = useState("");

  function handleShow() {
    if (!rollNo.trim()) {
      alert("Please enter your roll number.");
      return;
    }

    onShow(rollNo.trim());
  }

  return (
    <section className="section">

      <div className="section-heading">
        <div>
          <h2>My Bookings</h2>
          <p>View and manage your equipment bookings</p>
        </div>
      </div>

      <div className="search-box">

        <input
          type="text"
          placeholder="Enter your roll number"
          value={rollNo}
          onChange={(e) => setRollNo(e.target.value)}
        />

        <button
          className="primary-btn"
          onClick={handleShow}
        >
          Show Bookings
        </button>

      </div>

      <div className="booking-list">

        {bookings.map((booking) => (

          <div className="booking-card" key={booking.id}>

            <h3>{booking.equipment_name}</h3>

            <p>
              <strong>Booking ID:</strong> {booking.id}
            </p>

            <p>
              <strong>Roll Number:</strong> {booking.roll_no}
            </p>

            <p>
              <strong>Booking Date:</strong> {booking.booking_date}
            </p>

            <button
              className="cancel-btn"
              onClick={() => onCancel(booking.id)}
            >
              Cancel Booking
            </button>

          </div>

        ))}

        {bookings.length === 0 && (
          <p className="empty-message">
            No active bookings. Enter your roll number and click Show Bookings.
          </p>
        )}

      </div>

    </section>
  );
}

export default MyBookings;