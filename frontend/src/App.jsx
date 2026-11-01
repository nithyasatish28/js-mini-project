import { useState, useEffect } from "react";
import Events from "./components/Events";
import MyEvents from "./components/MyEvents";
import AddEvent from "./components/AddEvents";

const API_URL = "http://127.0.0.1:8001";

function App() {
  const [events, setEvents] = useState([]);
  const [page, setPage] = useState("events");

  async function loadEvents() {
    try {
      const response = await fetch(API_URL + "/events");
      const data = await response.json();
      setEvents(data);
    } catch (error) {
      console.log("Could not load events");
    }
  }

  useEffect(() => {
    loadEvents();
  }, []);

  async function registerEvent(eventId) {
    const rollNo = prompt("Enter your roll number:");

    if (!rollNo) {
      return;
    }

    try {
      const response = await fetch(
        API_URL + "/events/" + eventId + "/register",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            roll_no: rollNo
          })
        }
      );

      if (response.ok) {
        alert("Registration successful!");
        loadEvents();
      } else {
        const data = await response.json();
        alert(data.detail || "Registration failed");
      }
    } catch (error) {
      alert("Backend is not connected");
    }
  }

  async function addEvent(newEvent) {
    try {
      const response = await fetch(API_URL + "/events", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(newEvent)
      });

      if (response.ok) {
        alert("Event added successfully!");
        await loadEvents();
        setPage("events");
      } else {
        alert("Could not add event");
      }
    } catch (error) {
      alert("Backend is not connected");
    }
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

      {page === "addEvent" && <AddEvent onAdd={addEvent} />}
    </>
  );
}

export default App;