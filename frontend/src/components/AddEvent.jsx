import { useState } from "react";

function AddEvent({ onAdd }) {
  const [title, setTitle] = useState("");
  const [club, setClub] = useState("");
  const [category, setCategory] = useState("technical");
  const [date, setDate] = useState("");
  const [seats, setSeats] = useState("");

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
}

export default AddEvent;

