import { useState, useEffect } from "react";
import EventCard from "./EventCard";
import { API_URL } from "../config";

const CATEGORIES = ["All", "technical", "cultural", "sports", "workshop", "seminar"];

function EventList({ refresh, onUpdate }) {
  const [events, setEvents] = useState([]);
  const [category, setCategory] = useState("All");
  const [search, setSearch] = useState("");
  const [fetchError, setFetchError] = useState("");

  useEffect(() => {
    let url = `${API_URL}/events`;
    if (category !== "All") {
      url += `?category=${category}`;
    }

    fetch(url)
      .then((res) => {
        if (!res.ok) {
          throw new Error("Failed to load events");
        }
        return res.json();
      })
      .then((data) => {
        setEvents(data);
        setFetchError("");
      })
      .catch(() => {
        setFetchError("Could not connect to backend server.");
      });
  }, [refresh, category]);

  const filteredEvents = events.filter((ev) => {
    const term = search.toLowerCase();
    return (
      ev.title.toLowerCase().includes(term) ||
      ev.club.toLowerCase().includes(term)
    );
  });

  return (
    <div className="section">
      <h2>Campus Events</h2>

      {/* Category Filter */}
      <div className="category-filter">
        <label>Filter by Category:</label>
        {CATEGORIES.map((cat) => (
          <button
            key={cat}
            className={category === cat ? "active" : ""}
            onClick={() => setCategory(cat)}
          >
            {cat}
          </button>
        ))}
      </div>

      {/* Search Box */}
      <label>Search Events:</label>
      <input
        type="text"
        placeholder="Search by title or club name..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
      />

      {fetchError && <p className="error-message">{fetchError}</p>}

      {filteredEvents.length === 0 ? (
        <p>No events found.</p>
      ) : (
        filteredEvents.map((event) => (
          <EventCard
            key={event.id}
            event={event}
            onUpdate={onUpdate}
          />
        ))
      )}
    </div>
  );
}

export default EventList;
