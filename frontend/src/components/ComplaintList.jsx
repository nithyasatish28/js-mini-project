import ComplaintItem from "./ComplaintItem";

function ComplaintList({ complaints, onSelect, onMove, onDelete }) {
  return (
    <>
      <h1>Hostel Complaints</h1>
      <ul>
        {complaints.map((complaint) => (
          <ComplaintItem
            key={complaint.id}
            complaint={complaint}
            onSelect={onSelect}
            onMove={onMove}
            onDelete={onDelete}
          />
        ))}
      </ul>
    </>
  );
}

export default ComplaintList;