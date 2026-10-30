function ComplaintItem({ complaint, onSelect }) {
  return (
    <li className="product">
      <h2>Room {complaint.room_no} · {complaint.category}</h2>
      <p>{complaint.description}</p>
      <p>{complaint.status}</p>
      <p>{complaint.created_on}</p>
      <button onClick={() => onSelect(complaint.id)}>See updates</button>
    </li>
  );
}

export default ComplaintItem;