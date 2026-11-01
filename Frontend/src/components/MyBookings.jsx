import { useState } from "react";

function MyBookings({ API_URL }) {
  const [rollNo, setRollNo] = useState("");
  const [bookings, setBookings] = useState([]);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  // E6 - Show student bookings
  function showBookings() {
    if (rollNo.trim() === "") {
      setError("Please enter your roll number.");
      setMessage("");
      return;
    }

    fetch(`${API_URL}/bookings/student/${encodeURIComponent(rollNo.trim())}`)
      .then(async (response) => {
        const data = await response.json();
        if (!response.ok) {
          throw new Error(data.detail ?? `Request failed (${response.status})`);
        }
        return data;
      })
      .then((data) => {
        setBookings(data);
        setError("");
        if (data.length === 0) {
          setMessage("No active bookings found.");
        } else {
          setMessage("");
        }
      })
      .catch((requestError) => {
        setBookings([]);
        setMessage("");
        setError(requestError.message);
      });
  }

  // E7 - Cancel booking
  function cancelBooking(id) {
    fetch(`${API_URL}/booking/${id}/cancel`, {
      method: "PATCH",
    })
      .then(async (response) => {
        const data = await response.json();
        if (!response.ok) {
          throw new Error(data.detail ?? `Request failed (${response.status})`);
        }
        return data;
      })
      .then((data) => {
        setMessage(data.message || "Booking cancelled successfully.");
        setError("");
        showBookings();
      })
      .catch((requestError) => {
        setMessage("");
        setError(requestError.message);
      });
  }

  return (
    <section>
      <h2>My Bookings</h2>

      <p>
        <label>
          Roll number{" "}
          <input
            type="text"
            value={rollNo}
            onChange={(event) => setRollNo(event.target.value)}
          />
        </label>{" "}
        <button onClick={showBookings}>Show</button>
      </p>

      {error && <p role="alert">{error}</p>}
      {message && <p role="status">{message}</p>}

      {bookings.length > 0 && (
        <ul>
          {bookings.map((booking) => (
            <li key={booking.id}>
              <p>Equipment: {booking.equipment_name}</p>
              <p>Booking date: {booking.booking_date}</p>
              <button onClick={() => cancelBooking(booking.id)}>Cancel</button>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}

export default MyBookings;
