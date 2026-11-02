import { useState } from "react";
import { API_URL } from "../config";

function AddEvent({ onUpdate }) {
  const [title, setTitle] = useState("");
  const [club, setClub] = useState("");
  const [category, setCategory] = useState("technical");
  const [eventDate, setEventDate] = useState("");
  const [totalSeats, setTotalSeats] = useState("");

  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setSuccess("");

    if (!title.trim() || !club.trim()) {
      setError("Title and Club cannot be empty.");
      return;
    }

    if (!eventDate) {
      setError("Please select an event date.");
      return;
    }

    const seatsNum = Number(totalSeats);
    if (!seatsNum || seatsNum < 1 || seatsNum > 200) {
      setError("Total seats must be between 1 and 200.");
      return;
    }

    const newEvent = {
      title: title.trim(),
      club: club.trim(),
      category: category,
      event_date: eventDate,
      total_seats: seatsNum
    };

    try {
      const response = await fetch(`${API_URL}/events`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(newEvent)
      });

      const data = await response.json();

      if (!response.ok) {
        setError(data.detail || "Could not add event.");
        return;
      }

      setSuccess(data.message || "Event added successfully!");
      setTitle("");
      setClub("");
      setCategory("technical");
      setEventDate("");
      setTotalSeats("");
      onUpdate();
    } catch {
      setError("Could not connect to server.");
    }
  }

  return (
    <div className="section">
      <h2>Add New Event</h2>

      <form onSubmit={handleSubmit}>
        {error && <p className="error-message">{error}</p>}
        {success && <p className="success-message">{success}</p>}

        <label>Event Title:</label>
        <input
          type="text"
          placeholder="Title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          required
        />

        <label>Club Name:</label>
        <input
          type="text"
          placeholder="Club name"
          value={club}
          onChange={(e) => setClub(e.target.value)}
          required
        />

        <label>Category:</label>
        <select
          value={category}
          onChange={(e) => setCategory(e.target.value)}
        >
          <option value="technical">Technical</option>
          <option value="cultural">Cultural</option>
          <option value="sports">Sports</option>
          <option value="workshop">Workshop</option>
          <option value="seminar">Seminar</option>
        </select>

        <label>Event Date:</label>
        <input
          type="date"
          value={eventDate}
          onChange={(e) => setEventDate(e.target.value)}
          required
        />

        <label>Total Seats (1 - 200):</label>
        <input
          type="number"
          min="1"
          max="200"
          placeholder="Total seats"
          value={totalSeats}
          onChange={(e) => setTotalSeats(e.target.value)}
          required
        />

        <button type="submit">Add Event</button>
      </form>
    </div>
  );
}

export default AddEvent;
