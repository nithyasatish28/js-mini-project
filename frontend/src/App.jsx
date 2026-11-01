import { useState, useEffect } from "react";
import EventList from "./components/EventList";
import MyEvents from "./components/MyEvents";
import AddEvent from "./components/AddEvent";


const API_URL = "http://127.0.0.1:8001";
function App() {
  const [events, setEvents] = useState([]);
  const [registrations, setRegistrations] = useState([]);

  useEffect(() => {
    fetch(API_URL + "/events")
      .then((response) => response.json())
      .then((data) => setEvents(data));
  }, []);


  function filterEvents(category) {
    let url = API_URL + "/events";
    if (category !== "") {
      url = url + "?category=" + category;
    }
    fetch(url)
      .then((response) => response.json())
      .then((data) => setEvents(data));
  }

  
  function addEvent(title, club, category, eventDate, totalSeats) {
    fetch(API_URL + "/events?title=" + title + "&club=" + club + "&category=" + category + "&event_date=" + eventDate + "&total_seats=" + totalSeats, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title: title, club: club, category: category, event_date: eventDate, total_seats: totalSeats }),
    })
      .then((response) => response.json())
      .then(() => fetch(API_URL + "/events"))
      .then((response) => response.json())
      .then((data) => setEvents(data)); 
  }

  
  function deleteEvent(id) {
    fetch(API_URL + "/events/" + id, {
      method: "DELETE",
    })
      .then((response) => response.json())
      .then(() => fetch(API_URL + "/events"))
      .then((response) => response.json())
      .then((data) => setEvents(data)); 
  }


  function register(id, rollNo) {
    fetch(API_URL + "/events/" + id + "/registrations?roll_no=" + rollNo, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ roll_no: rollNo }),
    })
      .then((response) => response.json())
      .then(() => fetch(API_URL + "/events"))
      .then((response) => response.json())
      .then((data) => setEvents(data)); 
  }


  function showRegistrations(rollNo) {
    fetch(API_URL + "/registrations?roll_no=" + rollNo)
      .then((response) => response.json())
      .then((data) => setRegistrations(data));
  }


  function cancelRegistration(id, rollNo) {
    fetch(API_URL + "/registrations/" + id + "/cancel", {
      method: "PATCH",
    })
      .then((response) => response.json())
      .then(() => fetch(API_URL + "/registrations?roll_no=" + rollNo))
      .then((response) => response.json())
      .then((data) => setRegistrations(data)) 
      .then(() => fetch(API_URL + "/events"))
      .then((response) => response.json())
      .then((data) => setEvents(data)); 
  }

  return (
    <>
      <EventList events={events} onFilter={filterEvents} onRegister={register} onDelete={deleteEvent} />
      <MyEvents registrations={registrations} onShow={showRegistrations} onCancel={cancelRegistration} />
      <AddEvent onAdd={addEvent} />
    </>
  );
}

export default App;