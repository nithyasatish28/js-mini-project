function AddEvent() {
  return (
    <>
      <h2>Add New Event</h2>

      <input type="text" placeholder="Event Title" />

      <input type="text" placeholder="Club Name" />

      <input type="text" placeholder="Category" />

      <input type="date" />

      <input type="number" placeholder="Total Seats" />

      <button onClick={() => alert("Event added!")}>
        Add Event
      </button>
    </>
  );
}

export default AddEvent;