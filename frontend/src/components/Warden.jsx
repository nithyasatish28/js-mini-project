import { useState, useEffect } from "react";

function Warden({ API_URL, refresh, onAction }) {
  const [complaints, setComplaints] = useState([]);
  const [counts, setCounts] = useState({ open: 0, in_progress: 0, resolved: 0 });
  const [selectedStatus, setSelectedStatus] = useState("");
  const [selectedCategory, setSelectedCategory] = useState("");

  function fetchCounts() {
    fetch(`${API_URL}/complaints/stats/counts`)
      .then((res) => res.json())
      .then((data) => {
        setCounts(data);
      });
  }

  function fetchComplaints() {
    let url = `${API_URL}/complaints`;

    if (selectedStatus !== "" && selectedCategory !== "") {
      url = `${API_URL}/complaints?status=${selectedStatus}&category=${selectedCategory}`;
    } else if (selectedStatus !== "") {
      url = `${API_URL}/complaints?status=${selectedStatus}`;
    } else if (selectedCategory !== "") {
      url = `${API_URL}/complaints?category=${selectedCategory}`;
    }

    fetch(url)
      .then((res) => res.json())
      .then((data) => {
        setComplaints(data);
      });
  }

  useEffect(() => {
    fetchCounts();
    fetchComplaints();
  }, [refresh, selectedStatus, selectedCategory]);

  function changeStatus(id, currentStatus) {
    let nextStatus = "resolved";
    if (currentStatus === "open") {
      nextStatus = "in_progress";
    }

    fetch(`${API_URL}/complaints/${id}?new_status=${nextStatus}`, {
      method: "PATCH"
    })
      .then(() => {
        fetchCounts();
        fetchComplaints();
        onAction();
      });
  }

  return (
    <div className="card">
      <h2>Warden Dashboard</h2>

      <div className="stats-bar">
        Open: {counts.open} | In Progress: {counts.in_progress} | Resolved: {counts.resolved}
      </div>

      <div className="filter-section">
        <label>Filter by Status: <strong>{selectedStatus}</strong></label>
        <div className="button-group">
          <button type="button" onClick={() => setSelectedStatus("")}> All </button>
          <button type="button" onClick={() => setSelectedStatus("open")}> Open </button>
          <button type="button" onClick={() => setSelectedStatus("in_progress")}> In Progress </button>
          <button type="button" onClick={() => setSelectedStatus("resolved")}> Resolved </button>
        </div>
      </div>

      <div className="filter-section">
        <label>Filter by Category: <strong>{selectedCategory}</strong></label>
        <div className="button-group">
          <button type="button" onClick={() => setSelectedCategory("")}> All </button>
          <button type="button" onClick={() => setSelectedCategory("electrical")}> Electrical </button>
          <button type="button" onClick={() => setSelectedCategory("plumbing")}> Plumbing </button>
          <button type="button" onClick={() => setSelectedCategory("furniture")}> Furniture </button>
          <button type="button" onClick={() => setSelectedCategory("cleaning")}> Cleaning </button>
          <button type="button" onClick={() => setSelectedCategory("internet")}> Internet </button>
        </div>
      </div>

      <div className="complaint-list">
        {complaints.length === 0 && (
          <p>No complaints match your filters.</p>
        )}

        {complaints.map((complaint) => (
          <div key={complaint.id} className="warden-item">
            <div className="complaint-header">
              <div>
                <strong>Room {complaint.room_no}</strong> · Category: {complaint.category} · Roll No: {complaint.roll_no} · Status: {complaint.status}
              </div>

              {complaint.status !== "resolved" && (
                <button type="button" onClick={() => changeStatus(complaint.id, complaint.status)}> Move to next status </button>
              )}
            </div>
            <p><strong>Description:</strong> {complaint.description}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Warden;
