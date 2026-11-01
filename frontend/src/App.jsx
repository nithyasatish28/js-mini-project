import { useState, useEffect } from "react";
import "./App.css";
import AddEvent from "./components/AddEvents";
import MyEvents from "./components/MyEvents";

const API_URL = "http://127.0.0.1:8001";

function App() {
  const[events, setEvents] = useState([]);
  const[rollNo,setRollNo] = useState("");

  function getEvents() {
    fetch(API_URL + "/events")
      .then(response => response.json())
      .then(data => setEvents(data));
  }

  useEffect(function() {
    getEvents();
  }, []);

  return (
    <>
        <h1>Campus Event Registration</h1>
        <h2>Events</h2>
        <input placeholder="Enter Roll Number"
               value={rollNo}
               onChange={function(event) {
                   setRollNo(event.target.value);
              }}
        />
        {events.map(function(event) {
          return (
            <div className="event-card" key={event.id}>
                <h3>{event.title}</h3>
                <p>Club: {event.club}</p>
                <p>Category:{event.category}</p>
                <p>Date:{event.event_date}</p>
                <p>Seats Left: {event.seats_left}</p>

                <button onClick={functions(){
                  register(event.id);
            }}>
              Register
            </button>
            <button onClick={functions(){
              deleteEvent(event.id);
            }}> 
                Delete
            </button>
            </div>
          )
        })}
        <MyEvents rollNo={rollNo} />
        <AddEvent getEvents={getEvents}/>
    </>
  );
}
export default App;
