function ComplaintItem({ complaint, onSelect }) {
  let icon = "🔴";
  if (complaint.status === "in_progress") {
    icon = "🟡";
  }
  if (complaint.status === "resolved") {
    icon = "🟢";
  }

  return (
    <li>
      <h3>Room {complaint.room_no} · {complaint.category}</h3>
      <p><strong>Description:</strong> {complaint.description}</p>
      <p><strong>Status:</strong> {icon} {complaint.status}</p>
      <p><strong>Raised on:</strong> {complaint.created_on.slice(0, 10)}</p>
      <button onClick={() => onSelect(complaint.id)}>See updates</button>
      <hr />
    </li>
  );
}

export default ComplaintItem;