function Event({ event, apiUrl, onRefresh }) {
  const [rollNo, setRollNo] = useState("");
  const [error, setError] = useState("");
  const [msg, setMsg] = useState("");

  const today = new Date().toISOString().split("T")[0];
  const isPast = event.event_date < today;
  const isFull = event.seats_left <= 0;

  function handleRegister() {
    setError("");
    setMsg("");
    if (!rollNo.trim()) {
      setError("Please enter your roll number.");
      return;
    }
    fetch(`${apiUrl}/events/${event.id}/register?roll_no=${encodeURIComponent(rollNo.trim())}`, {
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.detail) {
          setError(data.detail);
        } else {
          setMsg("Registered successfully!");
          setRollNo("");
          onRefresh();
        }
      })
      .catch(() => setError("Cannot reach the server."));
  }

  function handleDelete() {
    setError("");
    setMsg("");
    fetch(`${apiUrl}/events/${event.id}`, {
      method: "DELETE",
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.detail) {
          setError(data.detail);
        } else {
          onRefresh();
        }
      })
      .catch(() => setError("Cannot reach the server."));
  }

  return (
    <li className="event-card">
      <h3>{event.title}</h3>
      <p><strong>Club:</strong> {event.club} | <strong>Category:</strong> {event.category}</p>
      <p><strong>Date:</strong> {event.event_date}</p>

      <div className="badge-row">
        <span className="badge badge-seats">{event.seats_left} seats left</span>
        {isFull && <span className="badge badge-full">Full</span>}
        {isPast && <span className="badge badge-past">Past</span>}
      </div>

      <div className="action-row">
        <input
          type="text"
          placeholder="Roll number"
          value={rollNo}
          onChange={(e) => setRollNo(e.target.value)}
          disabled={isPast || isFull}
        />
        <button
          className="btn-primary"
          onClick={handleRegister}
          disabled={isPast || isFull}
        >
          Register
        </button>
      </div>

      <button
        className="btn-danger"
        onClick={handleDelete}
        style={{ alignSelf: "flex-start" }}
      >
        Delete
      </button>

      {error && <p className="error">{error}</p>}
      {msg && <p className="success">{msg}</p>}
    </li>
  );
}

export default Card;
