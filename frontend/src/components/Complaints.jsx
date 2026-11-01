import { useState, useEffect } from "react";

function Complaints({ API_URL, refresh, onAction }) {
  const [rollNo, setRollNo] = useState("");
  const [complaints, setComplaints] = useState([]);
  const [selectedId, setSelectedId] = useState(null);
  const [updates, setUpdates] = useState([]);

  function fetchComplaints() {
    if (!rollNo) return;

    fetch(`${API_URL}/complaints/student/${rollNo}`)
      .then((res) => res.json())
      .then((data) => {
        setComplaints(data);
      });
  }

  useEffect(() => {
    if (rollNo) {
      fetchComplaints();
    }
  }, [refresh]);

  function toggleDetails(id) {
    if (selectedId === id) {
      setSelectedId(null);
      setUpdates([]);
      return;
    }

    fetch(`${API_URL}/complaints/${id}`)
      .then((res) => res.json())
      .then((data) => {
        setSelectedId(id);
        setUpdates(data.slice(1));
      });
  }

  function deleteComplaint(id) {
    fetch(`${API_URL}/complaints/${id}`, {
      method: "DELETE"
    })
      .then(() => {
        if (selectedId === id) {
          setSelectedId(null);
          setUpdates([]);
        }
        fetchComplaints();
        onAction();
      });
  }

  return (
    <div className="card">
      <h2>My Complaints</h2>

      <div className="filters">
        <input type="text" placeholder="Enter Roll Number" value={rollNo} onChange={(event) => setRollNo(event.target.value)} />
        <button type="button" onClick={fetchComplaints}> Show </button>
      </div>

      <div className="complaint-list">
        {complaints.length === 0 && rollNo && (
          <p>No complaints found for roll number {rollNo}.</p>
        )}

        {complaints.map((complaint) => (
          <div key={complaint.id} className="complaint-item" onClick={() => toggleDetails(complaint.id)}>
            <div className="complaint-header">
              <div>
                <strong>Room {complaint.room_no}</strong> · Category: {complaint.category} · Status: {complaint.status}
              </div>

              {complaint.status === "open" && (
                <button type="button" className="btn-delete" onClick={() => deleteComplaint(complaint.id)}> Delete </button>
              )}
            </div>

            {selectedId === complaint.id && (
              <div className="updates-box">
                <p><strong>Description:</strong> {complaint.description}</p>
                <h4>Updates:</h4>
                {updates.length === 0 && <p>No updates yet.</p>}
                {updates.length > 0 && (
                  <ul>
                    {updates.map((update) => (
                      <li key={update.id}>
                        Status updated to <strong>{update.status}</strong> {update.note}
                      </li>
                    ))}
                  </ul>
                )}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

export default Complaints;
