import { useState } from "react";

function MyComplaints({ apiUrl, onDone }) {
  const [roll_no, setRollNo] = useState("");
  const [complaints, setComplaints] = useState([]);
  const [updates, setUpdates] = useState([]);
  const [message, setMessage] = useState("");

  function searchComplaints() {
    if (roll_no.trim() === "") {
      setMessage("Enter a roll number");
      return;
    }

    fetch(apiUrl + "/students/" + encodeURIComponent(roll_no) + "/complaints")
      .then((response) => response.json())
      .then((data) => {
        setComplaints(data);
        setUpdates([]);
        setMessage("");
      });
  }

  function viewUpdates(id) {
    fetch(apiUrl + "/complaints/" + id)
      .then((response) => response.json())
      .then((data) => setUpdates(data.updates || []));
  }

  function deleteComplaint(id) {
    fetch(apiUrl + "/complaints/" + id, { method: "DELETE" }).then((response) => {
      if (response.ok) {
        setMessage("");
        setUpdates([]);
        setComplaints(complaints.filter((complaint) => complaint.id !== id));
        onDone();
      } else {
        response.json().then((data) => setMessage(data.detail));
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

      <p>{message}</p>

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