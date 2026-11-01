
function EventItem({ event, onRegister, onDelete }) {
  return (
    <li className="event">
      <h2>{event.title}</h2>
      <p>{event.club}</p>
      <p>{event.event_date}</p>
      <p>Seats left: {event.seats_left}</p>

      {event.seats_left > 0 ? (
        <button onClick={() => onRegister(event.id)}>Register</button>
      ) : (
        <p>Full</p>
      )}

      <button onClick={() => onDelete(event.id)}>Delete</button>
    </li>
  );
}

export default EventItem;