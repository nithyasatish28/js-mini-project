import { useState } from "react";

const CATEGORIES = ["technical", "cultural", "sports", "workshop", "seminar"];

function AddEvent({ onAdd }) {
  const [title, setTitle] = useState("");
  const [club, setClub] = useState("");
  const [category, setCategory] = useState(CATEGORIES[0]);
  const [eventDate, setEventDate] = useState("");
  const [totalSeats, setTotalSeats] = useState("");
  const [error, setError] = useState("");
  const [msg, setMsg] = useState("");


    fetch(`${apiUrl}/events?${queryParams.toString()}`, {
    
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.detail) {
          setError(data.detail);
        } else {
          setMsg(`Event "${data.title || title}" added successfully!`);
          setTitle("");
          setClub("");
          setCategory(CATEGORIES[0]);
          setEventDate("");
          setTotalSeats("");
          onRefresh();
        }
      })
      .catch(() => setError("Cannot reach the server."));
  }
 return (

    <>
      <h1>Add an event</h1>
      Title <input onChange={(e) => setTitle(e.target.value)} />
      Club <input onChange={(e) => setClub(e.target.value)} />
      <select onChange={(e) => setCategory(e.target.value)}>
        <option>technical</option>
        <option>cultural</option>
        <option>sports</option>
        <option>workshop</option>
        <option>seminar</option>
      </select>
      <input type="date" onChange={(e) => setDate(e.target.value)} />
      Seats <input type="number" onChange={(e) => setSeats(e.target.value)} />
      <button onClick={() => onAdd(title, club, category, date, seats)}>Add</button>
    </>
  );


export default AddEvent;