import { useState } from "react";

function MyComplaints({
  studentComplaints,
  complaint,
  message,
  getStudentComplaints,
  getComplaint,
  deleteComplaint,
}) {
  const [rollNo, setRollNo] = useState("");

  return (
    <>
      <h2>My complaints</h2>
      <input placeholder="Roll number" value={rollNo} onChange={(e) => setRollNo(e.target.value)} />
      <button onClick={() => getStudentComplaints(rollNo)}>Show</button>
      <p>{message}</p>

      {studentComplaints.map((c) => (
        <div key={c.id}>
          <p>Room | {c.room_no} |   ---   | {c.category} |</p>
          <p>{c.description}</p>
          <p>Status: {c.status}</p>
          <button onClick={() => getComplaint(c.id)}>View updates</button>
          {c.status === "open" && (
            <button onClick={() => deleteComplaint(c.id, rollNo)}>Delete</button>
          )}
        </div>
      ))}

      <h3>Updates</h3>
      {complaint.updates.map((update, index) => (
        <p key={index}>{update.status}: {update.note}</p>
      ))}
    </>
  );
}

export default MyComplaints;