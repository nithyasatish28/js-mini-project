import { useState } from "react";
import { API_URL } from "../config";

function EventCard({ event, onUpdate }) {
  const [rollNo, setRollNo] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const today = new Date().toISOString().split("T")[0];
  const isPast = event.event_date < today;
  const isFull = event.seats_left <= 0;

  async function handleRegister() {
    setError("");
    setSuccess("");

    if (!rollNo.trim()) {
      setError("Please enter your roll number first.");
      return;
    }

    try {
      const response = await fetch(`${API_URL}/events/${event.id}/registrations`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          roll_no: rollNo.trim()
        })
      });

      const data = await response.json();

      if (!response.ok) {
        setError(data.detail || "Registration failed.");
        return;
      }

      setSuccess(data.message || "Registration successful!");
      setRollNo("");
      onUpdate();
    } catch {
      setError("Could not connect to server.");
    }
  }

  async function handleDelete() {
    setError("");
    setSuccess("");

    try {
      const response = await fetch(`${API_URL}/events/${event.id}`, {
        method: "DELETE"
      });

      const data = await response.json();

      if (!response.ok) {
        setError(data.detail || "Could not delete event.");
        return;
      }

      onUpdate();
    } catch {
      setError("Could not connect to server.");
    }
  }

  return (
    <div className="event-card">
      <h3>{event.title}</h3>

      <p><strong>Club:</strong> {event.club}</p>
      <p><strong>Category:</strong> {event.category}</p>
      <p>
        <strong>Date:</strong> {event.event_date}
        {isPast && <span className="card-tag tag-past">Past Event</span>}
      </p>
      <p>
        <strong>Seats Left:</strong> {event.seats_left} / {event.total_seats}
        {isFull && <span className="card-tag tag-full">Full</span>}
      </p>

      {error && <p className="error-message">{error}</p>}
      {success && <p className="success-message">{success}</p>}

      <div style={{ marginTop: "10px" }}>
        <label htmlFor={`roll-${event.id}`}>Enter Roll Number:</label>
        <input
          id={`roll-${event.id}`}
          type="text"
          placeholder="e.g. 21BCE100"
          value={rollNo}
          disabled={isFull || isPast}
          onChange={(e) => {
            setRollNo(e.target.value);
            setError("");
            setSuccess("");
          }}
        />

        <button
          onClick={handleRegister}
          disabled={isFull || isPast}
        >
          {isFull ? "Full" : isPast ? "Event Over" : "Register"}
        </button>

        <button
          className="btn-danger"
          onClick={handleDelete}
        >
          Delete
        </button>
      </div>
    </div>
  );
}

export default EventCard;
