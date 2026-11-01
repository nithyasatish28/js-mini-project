import { useState } from "react";

function Warden({ complaints, counts, message, moveToNextStatus }) {
  const [note, setNote] = useState("");
  const [statusFilter, setStatusFilter] = useState("");
  const [categoryFilter, setCategoryFilter] = useState("");

  const shown = complaints.filter(
    (c) =>
      (statusFilter === "" || c.status === statusFilter) &&
      (categoryFilter === "" || c.category === categoryFilter)
  );

  return (
    <>
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

      <p>Type a note, then click Move on a complaint:</p>
      <input placeholder="Note" value={note} onChange={(e) => setNote(e.target.value)} />
      <p>{message}</p>

      {shown.map((c) => (
        <div key={c.id}>
          <p>Room {c.room_no} | {c.category} | Roll no: {c.roll_no}</p>
          <p>{c.description}</p>
          <p>Status: {c.status}</p>
          <button onClick={() => moveToNextStatus(c.id, note)}>Move to next status</button>
        </div>
      ))}
    </>
  );
}

export default Warden;