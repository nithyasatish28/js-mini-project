import { useState, useEffect } from "react";
import EventCard from "./components/EventCard";
import MyEvents from "./components/myevents";
import AddEvent from "./components/addevent";
import "./index.css";

const API_URL = "http://127.0.0.1:8001";

const CATEGORIES = ["", "technical", "cultural", "sports", "workshop", "seminar"];

function App() {
  const [events, setEvents] = useState([]);
  const [categoryFilter, setCategoryFilter] = useState("");

  function loadEvents(filter) {
    const url = filter
      ? `${API_URL}/events?category=${filter}`
      : `${API_URL}/events`;
    fetch(url)
      .then((res) => res.json())
      .then((data) => setEvents(data));
  }

  useEffect(() => {
    loadEvents(categoryFilter);
  }, [categoryFilter]);

  return (
    <>
      <div className="app-header">
        <h1>🎉 Campus Event Registration</h1>
      </div>

      <div className="section">
        <h2>Events</h2>
        <div className="filter-row">
          <label>Filter by category:</label>
          <select
            value={categoryFilter}
            onChange={(e) => setCategoryFilter(e.target.value)}
          >
            {CATEGORIES.map((cat) => (
              <option key={cat} value={cat}>
                {cat === "" ? "All Categories" : cat}
              </option>
            ))}
          </select>
        </div>

        <ul className="event-list">
          {events.map((event) => (
            <EventCard
              key={event.id}
              event={event}
              apiUrl={API_URL}
              onRefresh={() => loadEvents(categoryFilter)}
            />
          ))}
        </ul>
        {events.length === 0 && <p>No events found.</p>}
      </div>

      <div className="section">
        <MyEvents
          apiUrl={API_URL}
          onRefresh={() => loadEvents(categoryFilter)}
        />
      </div>

      <div className="section">
        <AddEvent
          apiUrl={API_URL}
          onRefresh={() => loadEvents(categoryFilter)}
        />
      </div>
    </>
  );
}

export default App;