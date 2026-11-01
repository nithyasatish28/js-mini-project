import { useState } from "react";

function Events(props) {
  const [category, setCategory] = useState("All");

  const filteredEvents =
    category === "All"
      ? props.events
      : props.events.filter(
    (event) => event.category.toLowerCase() === category.toLowerCase()
  );

  return (
    <>
      <h2>Available Events</h2>

      <label>Filter by Category: </label>

      <select
        value={category}
        onChange={(e) => setCategory(e.target.value)}
      >
        <option value="All">All</option>
        <option value="Technical">Technical</option>
        <option value="Cultural">Cultural</option>
        <option value="Sports">Sports</option>
      </select>

      {filteredEvents.map((event) => (
        <div key={event.id}>
          <h3>{event.title}</h3>
          <p>Club: {event.club}</p>
          <p>Category: {event.category}</p>
          <p>Date: {event.event_date}</p>
          <p>Available Seats: {event.seats_left}</p>

          <button onClick={() => props.onRegister(event.id)}>
            Register
          </button>
        </div>
      ))}
    </>
  );
}

export default Events;