import { useState } from "react";

function ComplaintItem({ complaint, onSelect, onMove, onDelete }) {
  const [note, setNote] = useState("");

  let icon = "🔴";
  if (complaint.status === "in_progress") {
    icon = "🟡";
  }
  if (complaint.status === "resolved") {
    icon = "🟢";
  }

  // the Delete button only shows on open complaints
  let deleteButton = null;
  if (complaint.status === "open") {
    deleteButton = <button onClick={() => onDelete(complaint.id)}>Delete</button>;
  }
 
  let resolvedLine = null;
  if (complaint.resolved_on !== null) {
    resolvedLine = <p><strong>Resolved on:</strong> {complaint.resolved_on.slice(0, 10)}</p>;
  }

  return (
    <li>
      <h3>Room {complaint.room_no} · {complaint.category}</h3>
      <p><strong>Roll no:</strong> {complaint.roll_no}</p>
      <p><strong>Description:</strong> {complaint.description}</p>
      <p><strong>Status:</strong> {icon} {complaint.status}</p>
      <p><strong>Raised on:</strong> {complaint.created_on.slice(0, 10)}</p>
      {resolvedLine}
      <button onClick={() => onSelect(complaint.id)}>See updates</button>
      {deleteButton}
      <p>
        <input value={note} onChange={(e) => setNote(e.target.value)} placeholder="Note" />
        <button onClick={() => onMove(complaint.id, note)}>Move to next status</button>
      </p>
      <hr />
    </li>
  );
}

export default ComplaintItem;