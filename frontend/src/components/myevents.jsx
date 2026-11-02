import { useState } from "react";

function MyEvents({ apiUrl, onRefresh }) {
  const [rollInput, setRollInput] = useState("");
  const [registrations, setRegistrations] = useState([]);
  const [searched, setSearched] = useState(false);
  const [error, setError] = useState("");
  const [msg, setMsg] = useState("");

  function handleShow() {
    setError("");
    setMsg("");
    if (!rollInput.trim()) {
      setError("Please enter your roll number.");
      return;
    }
    fetch(`${apiUrl}/registrations/${encodeURIComponent(rollInput.trim())}`)
      .then((res) => res.json())
      .then((data) => {
        if (data.detail) {
          setError(data.detail);
        } else {
          setRegistrations(data);
          setSearched(true);
        }
      })
      .catch(() => setError("Cannot reach the server."));
  }

  function handleCancel(regId) {
    setError("");
    setMsg("");
    fetch(`${apiUrl}/registrations/${regId}/cancel`, {
      method: "PATCH",
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.detail && !data.message) {
          setError(data.detail);
        } else {
          setMsg("Registration cancelled.");
          handleShow();
          if (onRefresh) onRefresh();
        }
      })
      .catch(() => setError("Cannot reach the server."));
  }

  return (
    <>
      <h2>My Events</h2>
      <div className="action-row" style={{ marginBottom: "16px" }}>
        <input
          type="text"
          placeholder="Your roll number"
          value={rollInput}
          onChange={(e) => setRollInput(e.target.value)}
        />
        <button className="btn-primary" onClick={handleShow}>Show</button>
      </div>

      {error && <p className="error">{error}</p>}
      {msg && <p className="success">{msg}</p>}

      <ul className="reg-list">
        {registrations.map((reg) => (
          <li key={reg.id} className="reg-item">
            <div>
              <p><strong>{reg.title || `Event #${reg.event_id}`}</strong></p>
              <p>Date: {reg.event_date || "Upcoming"} | Reg ID: #{reg.id}</p>
            </div>
            <button className="btn-danger" onClick={() => handleCancel(reg.id)}>
              Cancel
            </button>
          </li>
        ))}
      </ul>

      {searched && registrations.length === 0 && (
        <p>No active registrations found for this roll number.</p>
      )}
    </>
  );
}

export default MyEvents;