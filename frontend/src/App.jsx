import { useState, useEffect } from "react";
import EventList from "./components/EventList";
import MyEvents from "./components/MyEvents";
import AddEvent from "./components/AddEvent";


const API_URL = "http://127.0.0.1:8001";
function App() {
  const [events, setEvents] = useState([]);
  const [registrations, setRegistrations] = useState([]);
  const [rollNo, setRollNo] = useState("");

  useEffect(() => {
    fetch(API_URL + "/events")
      .then((response) => response.json())
      .then((data) => setEvents(data));
  }, []);


  function filterEvents(category) {
    fetch(API_URL + "/events" + (category ? "?category=" + category : ""))
      .then((response) => response.json())
      .then((data) => setEvents(data));
  }

  
  function addEvent(title, club, category, date, seats) {
    fetch(API_URL + "/events?title=" + title + "&club=" + club + "&category=" + category + "&event_date=" + date + "&total_seats=" + seats, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title: title, club: club, category: category, event_date: date, total_seats: seats }),
    })
      .then(() => fetch(API_URL + "/events"))
      .then((response) => response.json())
      .then((data) => setEvents(data));
  }


  function deleteEvent(id) {
    fetch(API_URL + "/events/" + id, { method: "DELETE" })
      .then(() => fetch(API_URL + "/events"))
      .then((response) => response.json())
      .then((data) => setEvents(data));
  }


  function register(id) {
    fetch(API_URL + "/events/" + id + "/registrations?roll_no=" + rollNo, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ roll_no: rollNo }),
    })
      .then(() => fetch(API_URL + "/events"))
      .then((response) => response.json())
      .then((data) => setEvents(data));
  }


  function showRegistrations(roll) {
    fetch(API_URL + "/registrations?roll_no=" + roll)
      .then((response) => response.json())
      .then((data) => setRegistrations(data));
  }


  function cancelRegistration(id, roll) {
    fetch(API_URL + "/registrations/" + id + "/cancel", { method: "PATCH" })
      .then(() => showRegistrations(roll))
      .then(() => fetch(API_URL + "/events"))
      .then((response) => response.json())
      .then((data) => setEvents(data));
  }

  return (
    <>
      <select onChange={(e) => filterEvents(e.target.value)}>
        <option value="">all</option>
        {["technical", "cultural", "sports", "workshop", "seminar"].map((c) => <option key={c}>{c}</option>)}
      </select>
      Roll number <input onChange={(e) => setRollNo(e.target.value)} />
      <EventList events={events} onRegister={register} onDelete={deleteEvent} />
      <MyEvents registrations={registrations} onShow={showRegistrations} onCancel={cancelRegistration} />
      <AddEvent onAdd={addEvent} />
    </>
  );
}

export default App;