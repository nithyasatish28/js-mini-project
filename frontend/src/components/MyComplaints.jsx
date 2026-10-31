import { useState } from "react";

const API_URL = "http://127.0.0.1:8001";

function MyComplaints() {
  const [roll_no, setRollNo] = useState("");
  const [complaints, setComplaints] = useState([]);
  const [updates, setUpdates] = useState([]);

  function searchComplaints() {
    fetch(API_URL + "/students/" + roll_no + "/complaints")
      .then((response) => response.json())
      .then((data) => setComplaints(data));
  }

  function viewUpdates(id) {
    fetch(API_URL + "/complaints/" + id)
      .then((response) => response.json())
      .then((data) => setUpdates(data.updates || []));
  }

  function deleteComplaint(id) {
    fetch(API_URL + "/complaints/" + id, {
      method: "DELETE"
    }).then((response) => {
      if (response.ok) {
        setComplaints(
          complaints.filter((complaint) => complaint.id !== id)
        );
      }
    });
  }

  return (
    <div>
      <h2>My Complaints</h2>

      <input placeholder="Enter roll number"
        value={roll_no}
        onChange={(e) => setRollNo(e.target.value)} />

      <button onClick={searchComplaints}>Search</button>

      {complaints.map((complaint) => (
        <div key={complaint.id}>
          <hr />
          <p>Room: {complaint.room_no}</p>
          <p>Category: {complaint.category}</p>
          <p>{complaint.description}</p>
          <p>Status: {complaint.status}</p>

          <button onClick={() => viewUpdates(complaint.id)}>
            View Updates
          </button>

          {complaint.status === "open" && (
            <button onClick={() => deleteComplaint(complaint.id)}>
              Delete
            </button>
          )}
        </div>
      ))}

      {updates.map((update, index) => (
        <p key={index}>
          {update.status}: {update.note}
        </p>
      ))}
    </div>
  );
}

export default MyComplaints;