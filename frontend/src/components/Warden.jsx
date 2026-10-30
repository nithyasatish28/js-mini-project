function Warden({ complaints }) {
  return (
    <div>
      <h2>Warden</h2>
      {complaints.map((c) => (
        <div key={c.id}>
          {c.room_no} - {c.category} - {c.status}
        </div>
      ))}
    </div>
  );
}

export default Warden; 