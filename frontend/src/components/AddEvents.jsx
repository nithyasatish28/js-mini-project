
import { useState } from "react";

function AddEvent(props) {
  const [title, setTitle] = useState("");
  const [club, setClub] = useState("");
  const [category, setCategory] = useState("");
  const [eventDate, setEventDate] = useState("");
  const [totalSeats, setTotalSeats] = useState("");

  function addEvent() {
    if (
      title === "" ||
      club === "" ||
      category === "" ||
      eventDate === "" ||
      totalSeats === ""
    ) {
      alert("Please fill all the fields");
      return;
    }

    if (Number(totalSeats) <= 0) {
      alert("Total seats must be greater than 0");
      return;
    }

    const newEvent = {
      title: title,
      club: club,
      category: category,
      event_date: eventDate,
      total_seats: Number(totalSeats)
    };

    props.onAdd(newEvent);

    setTitle("");
    setClub("");
    setCategory("");
    setEventDate("");
    setTotalSeats("");
  }

  return (
    <>
      <h2>Add New Event</h2>

      <input
        type="text"
        placeholder="Event Title"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
      />

      <input
        type="text"
        placeholder="Club Name"
        value={club}
        onChange={(e) => setClub(e.target.value)}
      />

      <input
        type="text"
        placeholder="Category"
        value={category}
        onChange={(e) => setCategory(e.target.value)}
      />

      <input
        type="date"
        value={eventDate}
        onChange={(e) => setEventDate(e.target.value)}
      />

      <input
        type="number"
        placeholder="Total Seats"
        value={totalSeats}
        onChange={(e) => setTotalSeats(e.target.value)}
      />

      <button onClick={addEvent}>Add Event</button>
    </>
  );
}

export default AddEvent;
