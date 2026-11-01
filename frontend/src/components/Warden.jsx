import { useState } from "react";

function WardenItem({ complaint, moveToNextStatus }) {
  const [note, setNote] = useState("");

  return (
    <div>
      <hr />
    
      <p>Room | {complaint.room_no} |   ---   | {complaint.category} |   ---   | Roll no: {complaint.roll_no} |</p>
      <p>{complaint.description}</p>
      <p>Status: {complaint.status}</p>
  

      {complaint.status !== "resolved" && (
        <>
          <input placeholder="Note" value={note} onChange={(e) => setNote(e.target.value)} />
          <button
            onClick={() => {
              moveToNextStatus(complaint.id, note);
              setNote("");
            }}
          >
            Move to next status
          </button>
        </>
      )}
    </div>
  );
}

function Warden({ complaints, counts, message, moveToNextStatus }) {
  const [statusFilter, setStatusFilter] = useState("");
  const [categoryFilter, setCategoryFilter] = useState("");

  const shown = complaints.filter(
    (c) =>
      (statusFilter === "" || c.status === statusFilter) &&
      (categoryFilter === "" || c.category === categoryFilter)
  );

  return (
    <>
      <h1>Warden</h1>
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
        <WardenItem key={c.id} complaint={c} moveToNextStatus={moveToNextStatus} />
      ))}
    </>
  );
}

export default Warden;