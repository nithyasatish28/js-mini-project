import EventItem from "./EventItem";

function EventList({ events, onRegister, onDelete }) {
  return (
    <>
      <h1>Events</h1>
      <ul className="events">
        {events.map((event) => (
          <EventItem key={event.id} event={event} onRegister={onRegister} onDelete={onDelete} />
        ))}
      </ul>
    </>
  );
}

export default EventList;


