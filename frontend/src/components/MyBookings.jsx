import { useState } from "react";

function MyBookings({ apiUrl }) {
  const [rollInput, setRollInput] = useState("");
  const [bookings, setBookings] = useState([]);
  const [error, setError] = useState("");
  const [msg, setMsg] = useState("");
  const [searched, setSearched] = useState(false);

  function handleShow() {
    setError("");
    setMsg("");
    if (!rollInput.trim()) {
      setError("Enter your roll number.");
      return;
    }
    fetch(`${apiUrl}/booking/${encodeURIComponent(rollInput.trim())}`)
      .then((res) => res.json())
      .then((data) => {
        setSearched(true);
        if (data.detail) {
          setError(data.detail);
          setBookings([]);
        } else {
          setBookings(data);
          if (data.length === 0) {
            setMsg("No active bookings.");
          }
        }
      })
      .catch(() => {
        setError("Failed to fetch bookings.");
      });
  }

  function handleCancel(bookingId) {
    setError("");
    setMsg("");
    fetch(`${apiUrl}/booking/cancel/${encodeURIComponent(rollInput.trim())}?booking_id=${bookingId}`, {
      method: "PATCH",
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.detail && !data.message) {
          setError(data.detail);
        } else {
          setMsg("Booking cancelled.");
          handleShow();
        }
      })
      .catch(() => {
        setError("Failed to cancel booking.");
      });
  }

  return (
    <>
      <h2>My Bookings</h2>
      <div className="book-row">
        <input
          type="text"
          placeholder="Your roll number"
          value={rollInput}
          onChange={(e) => {
            setRollInput(e.target.value);
            setSearched(false);
          }}
        />
        <button className="btn-primary" onClick={handleShow}>Show</button>
      </div>

      {error && <p className="error">{error}</p>}
      {msg && <p className="success">{msg}</p>}

      <ul className="booking-list">
        {bookings.map((b) => (
          <li key={b.id} className="booking-item">
            <div>
              <p>
                <strong>Booking #{b.id}</strong>{" "}
                {b.cancelled === 1 ? (
                  <span className="badge">Cancelled</span>
                ) : null}
              </p>
              <p>
                {b.equipment_name ? `${b.equipment_name} | ` : ""}
                Equipment ID: {b.equipment_id} | Date: {b.booking_date}
              </p>
            </div>
            {b.cancelled === 0 && (
              <button className="btn-danger" onClick={() => handleCancel(b.id)}>
                Cancel
              </button>
            )}
          </li>
        ))}
      </ul>
      {searched && !error && !msg && bookings.length === 0 && (
        <p>This roll number doesn't have any bookings.</p>
      )}
    </>
  );
}

export default MyBookings;
