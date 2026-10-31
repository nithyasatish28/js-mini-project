import ComplaintItem from "./ComplaintItem";

function ComplaintList({ complaints, onSelect }) {
  return (
    <>
      <h1>Hostel Complaints</h1>
<ul>
        {complaints.map((complaint) => (
          <ComplaintItem key={complaint.id} complaint={complaint} onSelect={onSelect} />
        ))}
      </ul>
    </>
  );
}

export default ComplaintList;