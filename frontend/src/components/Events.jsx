import { useState } from "react";

function Events(props) {
  const [category, setCategory] = useState("All");

  const filteredEvents = category === "All" 
    ? props.events 
    : props.events.filter((e) => e.category === category);

  return (
    <div>
      <select onChange={(e) => setCategory(e.target.value)}>
        <option value="All">All</option>
        <option value="technical">Technical</option>
        <option value="cultural">Cultural</option>
        <option value="sports">Sports</option>
        <option value="workshop">Workshop</option>
        <option value="seminar">Seminar</option>
      </select>

      {filteredEvents.map((e) => (
        <div key={e.id} style={{ border: "1px solid #ccc", margin: "5px", padding: "5px" }}>
          <h3>{e.title}</h3>
          <p>{e.club} | {e.category} | {e.event_date} | Seats: {e.seats_left}</p>
          <button onClick={() => props.onDelete(e.id)}>Delete</button>
        </div>
      ))}
    </div>
  );
}

export default Events;