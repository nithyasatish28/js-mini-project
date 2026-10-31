import { useState } from "react";

function Warden({ complaints, counts, apiUrl, onDone }) {
  const [notes, setNotes] = useState({});
  const [message, setMessage] = useState("");
  const [statusFilter, setStatusFilter] = useState("");
  const [categoryFilter, setCategoryFilter] = useState("");

  function changeNote(id, value) {
    setNotes({ ...notes, [id]: value });
  }

  function moveNext(id) {
    const note = notes[id] || "";

    fetch(apiUrl + "/complaints/" + id + "/status?note=" + encodeURIComponent(note), {
      method: "PATCH",
    })
      .then((response) => response.json().then((data) => ({ ok: response.ok, data })))
      .then((result) => {
        if (result.ok) {
          setMessage("");
          setNotes({ ...notes, [id]: "" });
          onDone();
        } else {
          setMessage(result.data.detail);
        }
      });
  }

  const shown = complaints.filter((c) => {
    if (statusFilter !== "" && c.status !== statusFilter) return false;
    if (categoryFilter !== "" && c.category !== categoryFilter) return false;
    return true;
  });

  return (
    <div>
      <h2>Warden</h2>
      <p>Open: {counts.open} | In progress: {counts.in_progress} | Resolved: {counts.resolved}</p>

      <select value={statusFilter} onChange={(e) => setStatusFilter(e.target.value)}>
        <option value="">All statuses</option>
        <option value="open">open</option>
        <option value="in_progress">in_progress</option>
        <option value="resolved">resolved</option>
      </select>

      <select value={categoryFilter} onChange={(e) => setCategoryFilter(e.target.value)}>
        <option value="">All categories</option>
        <option value="electrical">electrical</option>
        <option value="plumbing">plumbing</option>
        <option value="furniture">furniture</option>
        <option value="cleaning">cleaning</option>
        <option value="internet">internet</option>
      </select>

      <p>{message}</p>

      {shown.map((c) => (
        <div key={c.id}>
          <p>Room {c.room_no} | {c.category} | Roll no: {c.roll_no}</p>
          <p>{c.description}</p>
          <p>Status: {c.status}</p>

          {c.status !== "resolved" && (
            <div>
              <input
                placeholder="Note"
                value={notes[c.id] || ""}
                onChange={(e) => changeNote(c.id, e.target.value)}
              />
              <button onClick={() => moveNext(c.id)}>Move to next status</button>
            </div>
          )}
        </div>
      ))}
    </div>
  );
}

export default Warden;