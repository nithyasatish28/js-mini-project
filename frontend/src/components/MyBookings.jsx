import { useState } from "react";

function MyBookings({ apiUrl }) {
  const [rollInput, setRollInput] = useState("");
  const [bookings, setBookings] = useState([]);
  const [error, setError] = useState("");
  const [msg, setMsg] = useState("");

  const today = new Date().toISOString().split("T")[0];

  function handleShow() {
    setError("");
    setMsg("");
    if (!rollInput) {
      setError("Enter your roll number.");
      return;
    }
    fetch(`${apiUrl}/booking/${rollInput}`)
      .then((res) => res.json())
      .then((data) => {
        if (data.detail) {
          setError(data.detail);
        } else {
          setBookings(data);
        }
      });
  }

  function handleCancel(bookingId) {
    setError("");
    setMsg("");
    fetch(`${apiUrl}/booking/cancel/${rollInput}?booking_id=${bookingId}`, {
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
      });
  }

  const active = bookings.filter(
    (b) => b.cancelled === 0 && b.booking_date >= today
  );

  return (
    <>
      <h2>My Bookings</h2>
      <div className="book-row">
        <input
          type="text"
          placeholder="Your roll number"
          value={rollInput}
          onChange={(e) => setRollInput(e.target.value)}
        />
        <button className="btn-primary" onClick={handleShow}>Show</button>
      </div>

      {error && <p className="error">{error}</p>}
      {msg && <p className="success">{msg}</p>}


    </>
  );
}

export default MyBookings;