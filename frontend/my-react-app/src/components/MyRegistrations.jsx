import { useState } from "react";
import { API_URL } from "../config";

function MyRegistrations({ onUpdate }) {
  const [rollNo, setRollNo] = useState("");
  const [registrations, setRegistrations] = useState([]);
  const [searched, setSearched] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  async function handleShow(e) {
    if (e) e.preventDefault();
    setError("");
    setSuccess("");

    if (!rollNo.trim()) {
      setError("Please enter your roll number first.");
      return;
    }

    try {
      const response = await fetch(`${API_URL}/registrations/${encodeURIComponent(rollNo.trim())}`);
      const data = await response.json();

      if (!response.ok) {
        setError(data.detail || "Could not fetch registrations.");
        return;
      }

      setRegistrations(data);
      setSearched(true);
    } catch {
      setError("Could not connect to server.");
    }
  }

  async function handleCancel(registrationId) {
    setError("");
    setSuccess("");

    try {
      const response = await fetch(`${API_URL}/registrations/${registrationId}/cancel`, {
        method: "PATCH"
      });

      const data = await response.json();

      if (!response.ok) {
        setError(data.detail || "Could not cancel registration.");
        return;
      }

      setSuccess(data.message || "Registration cancelled successfully.");
      handleShow();
      onUpdate();
    } catch {
      setError("Could not connect to server.");
    }
  }

  return (
    <div className="section">
      <h2>My Registrations</h2>

      <form onSubmit={handleShow}>
        <label htmlFor="reg-roll-input">Enter Roll Number:</label>
        <input
          id="reg-roll-input"
          type="text"
          placeholder="e.g. 21BCE100"
          value={rollNo}
          onChange={(e) => {
            setRollNo(e.target.value);
            setError("");
            setSuccess("");
          }}
        />
        <button type="submit">Show</button>
      </form>

      {error && <p className="error-message">{error}</p>}
      {success && <p className="success-message">{success}</p>}

      {searched && (
        <div style={{ marginTop: "15px" }}>
          {registrations.length === 0 ? (
            <p>No active registrations found for roll number <strong>{rollNo}</strong>.</p>
          ) : (
            registrations.map((item) => (
              <div className="event-card" key={item.registration_id}>
                <h3>{item.title}</h3>
                <p><strong>Date:</strong> {item.event_date}</p>
                <p><strong>Registration ID:</strong> #{item.registration_id}</p>

                <button
                  className="btn-danger"
                  style={{ marginLeft: "0px", marginTop: "8px" }}
                  onClick={() => handleCancel(item.registration_id)}
                >
                  Cancel Registration
                </button>
              </div>
            ))
          )}
        </div>
      )}
    </div>
  );
}

export default MyRegistrations;
