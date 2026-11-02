import {useState,useEffect}from"react";
import Events from"./components/Events";
import AddEvent from"./components/AddEvent";

const API_URL = "http://127.0.0.1:8001";

function App() {
  const [events, setEvents] = useState([]);
  const [tab, setTab] = useState("view");

  function loadEvents() {
    fetch(API_URL + "/events")
      .then((res) => res.json())
      .then((data) => setEvents(data));
  }

  useEffect(() => { loadEvents(); }, []);

  function handleAddEvent(data) {
    const q = "title=" + data.title + "&club=" + data.club + "&category=" + data.category + "&event_date=" + data.event_date + "&total_seats=" + data.total_seats;
    fetch(API_URL + "/events?" + q, { method: "POST" })
      .then((res) => res.json())
      .then(() => { loadEvents(); setTab("view"); });
  }

  function handleDeleteEvent(id) {
    fetch(API_URL + "/events/" + id, { method: "DELETE" })
      .then((res) => res.json())
      .then(() => loadEvents());
  }

  return (
    <div>
      <button onClick={() => setTab("view")}>View Events</button>
      <button onClick={() => setTab("add")}>Add Event</button>
      {tab === "view" ? <Events events={events} onDelete={handleDeleteEvent} /> : <AddEvent onAddEvent={handleAddEvent} />}
    </div>
  );
}

export default App;