import { useState, useEffect } from "react";
import Events from "./components/Events";
import MyEvents from "./components/MyEvents";
import AddEvent from "./components/AddEvent";

const API_URL = "http://127.0.0.1:8001";

function App() {
  const [events, setEvents] = useState([]);
  const [page, setPage] = useState("events");

  useEffect(() => {
    fetch(API_URL + "/events")
      .then((response) => response.json())
      .then((data) => setEvents(data));
  }, []);

  function registerEvent(eventId) {
    alert("Registration clicked for event " + eventId);
  }

  return (
    <>
      <h1>Campus Event Registration</h1>

      <button onClick={() => setPage("events")}>Events</button>

      <button onClick={() => setPage("myEvents")}>My Events</button>

      <button onClick={() => setPage("addEvent")}>Add Event</button>

      {page === "events" && (
        <Events events={events} onRegister={registerEvent} />
      )}

      {page === "myEvents" && <MyEvents />}

      {page === "addEvent" && <AddEvent />}
    </>
  );
}

export default App;