import { useState } from "react";

const API_URL = "http://127.0.0.1:8001";

function MyEvents() {
  const [rollNo, setRollNo] = useState("");
  const [myEvents, setMyEvents] = useState([]);

  async function findEvents() {
    if (rollNo === "") {
      alert("Please enter your roll number");
      return;
    }

    try {
      const response = await fetch(
        API_URL + "/students/" + rollNo + "/registrations"
      );

      if (!response.ok) {
        alert("Could not find registrations");
        return;
      }

      const data = await response.json();
      setMyEvents(data);
    } catch (error) {
      alert("Backend is not connected");
    }
  }

  return (
    <>
      <h2>My Registered Events</h2>

      <input
        type="text"
        placeholder="Enter your roll number"
        value={rollNo}
        onChange={(e) => setRollNo(e.target.value)}
      />

      <button onClick={findEvents}>View My Events</button>

      {myEvents.map((event) => (
        <div key={event.id}>
          <h3>{event.title}</h3>
          <p>Category: {event.category}</p>
          <p>Date: {event.event_date}</p>
        </div>
      ))}
    </>
  );
}

export default MyEvents;