import ComplaintItem from "./ComplaintItem";

function ComplaintList({ complaints }) {
  return (
    <>
      <h1>All Complaints</h1>

      <ul>
        {complaints.map((complaint) => (
          <ComplaintItem
            key={complaint.id}
            complaint={complaint}
          />
        ))}
      </ul>
    </>
  );
}

export default ComplaintList;