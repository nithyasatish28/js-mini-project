import { useState } from "react";

function MyBookings({ bookings, onShow, onCancel }) {

  const [rollNo, setRollNo] = useState("");

  return (
    <>
      <h1>My Bookings</h1>

      <input
        type="text"
        placeholder="Enter Roll Number"
        value={rollNo}
        onChange={(e) => setRollNo(e.target.value)}
      />

      <button onClick={() => onShow(rollNo)}>
        Show
      </button>

      <ul>
        {bookings.map((booking) => (
          <li key={booking.id}>
            <h2>{booking.equipment_name}</h2>

            <p>Booking Date: {booking.booking_date}</p>
            <p>Roll Number: {booking.roll_no}</p>

            <button onClick={() => onCancel(booking.id, rollNo)}>
              Cancel
            </button>
          </li>
        ))}
      </ul>
    </>
  );
}

export default MyBookings;