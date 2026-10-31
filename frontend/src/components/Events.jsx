function Events(props) {
  return (
    <>
      <h2>Available Events</h2>

      {props.events.map((event) => (
        <div key={event.id}>
          <h3>{event.title}</h3>
          <p>Club: {event.club}</p>
          <p>Category: {event.category}</p>
          <p>Date: {event.event_date}</p>
          <p>Available Seats: {event.seats_left}</p>
          <button onClick={() => alert("Registration clicked!")}>
  Register
</button>
        </div>
      ))}
    </>
  );
}

export default Events;