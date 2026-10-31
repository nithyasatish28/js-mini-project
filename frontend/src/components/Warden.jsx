function Warden({ complaints, counts }) {
  return (
    <div>
      <h2>Warden</h2>
      <p>Open: {counts.open} | In progress: {counts.in_progress} | Resolved: {counts.resolved}</p>

      {complaints.map((c) => (
        <div key={c.id}>
          <p>Room {c.room_no} | {c.category} | Roll no: {c.roll_no}</p>
          <p>{c.description}</p>
          <p>Status: {c.status}</p>
        </div>
      ))}
    </div>
  );
}

export default Warden;