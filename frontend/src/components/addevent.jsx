import { useState } from "react";

const CATEGORIES = ["technical", "cultural", "sports", "workshop", "seminar"];

function AddEvent({ apiUrl, onRefresh }) {
  const [title, setTitle] = useState("");
  const [club, setClub] = useState("");
  const [category, setCategory] = useState(CATEGORIES[0]);
  const [eventDate, setEventDate] = useState("");
  const [totalSeats, setTotalSeats] = useState("");
  const [error, setError] = useState("");
  const [msg, setMsg] = useState("");

  function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setMsg("");

    if (!title.trim() || !club.trim() || !eventDate || !totalSeats) {
      setError("All fields are required.");
      return;
    }

    const seatsNum = parseInt(totalSeats, 10);
    if (isNaN(seatsNum) || seatsNum < 1 || seatsNum > 200) {
      setError("Total seats must be between 1 and 200.");
      return;
    }

    const queryParams = new URLSearchParams({
      title: title.trim(),
      club: club.trim(),
      category: category,
      event_date: eventDate,
      total_seats: seatsNum,
    });

    fetch(`${apiUrl}/events?${queryParams.toString()}`, {
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.detail) {
          setError(data.detail);
        } else {
          setMsg(`Event "${data.title || title}" added successfully!`);
          setTitle("");
          setClub("");
          setCategory(CATEGORIES[0]);
          setEventDate("");
          setTotalSeats("");
          onRefresh();
        }
      })
      .catch(() => setError("Cannot reach the server."));
  }

  return (
    <>
      <h2>Add an Event</h2>
      <form className="add-form" onSubmit={handleSubmit}>
        <div>
          <label>Event Title</label>
          <input
            type="text"
            placeholder="e.g. AI & Robotics Expo"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
          />
        </div>

        <div>
          <label>Club Name</label>
          <input
            type="text"
            placeholder="e.g. Robotics Club"
            value={club}
            onChange={(e) => setClub(e.target.value)}
          />
        </div>

        <div>
          <label>Category</label>
          <select value={category} onChange={(e) => setCategory(e.target.value)}>
            {CATEGORIES.map((cat) => (
              <option key={cat} value={cat}>
                {cat}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label>Event Date</label>
          <input
            type="date"
            value={eventDate}
            onChange={(e) => setEventDate(e.target.value)}
          />
        </div>

        <div>
          <label>Total Seats (1 to 200)</label>
          <input
            type="number"
            min="1"
            max="200"
            placeholder="e.g. 50"
            value={totalSeats}
            onChange={(e) => setTotalSeats(e.target.value)}
          />
        </div>

        <button type="submit" className="btn-primary" style={{ alignSelf: "flex-start" }}>
          Add Event
        </button>
      </form>

      {error && <p className="error">{error}</p>}
      {msg && <p className="success">{msg}</p>}
    </>
  );
}

export default AddEvent;