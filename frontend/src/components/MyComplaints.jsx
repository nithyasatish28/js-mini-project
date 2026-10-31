import { useState } from "react";
import { API_URL } from "../api";

function MyComplaints() {
    const [rollNo, setRollNo] = useState("");
    const [complaints, setComplaints] = useState([]);
    const [selectedComplaint, setSelectedComplaint] = useState(null);
    const [error, setError] = useState("");

    async function showComplaints() {
        const response = await fetch(
            `${API_URL}/students/${encodeURIComponent(rollNo)}/complaints`
        );

        const data = await response.json();

        if (response.ok) {
            setComplaints(data);
            setSelectedComplaint(null);
            setError("");
        } else {
            setError(data.detail);
        }
    }

    async function viewUpdates(id) {
        const response = await fetch(`${API_URL}/complaints/${id}`);
        const data = await response.json();

        if (response.ok) {
            setSelectedComplaint(data);
            setError("");
        } else {
            setError(data.detail);
        }
    }

    async function deleteComplaint(id) {
        const response = await fetch(`${API_URL}/complaints/${id}`, {
            method: "DELETE"
        });

        const data = await response.json();

        if (response.ok) {
            setError("");
            setSelectedComplaint(null);
            showComplaints();
        } else {
            setError(data.detail);
        }
    }

    return (
    <div className="dashboard-card">
            <h2>My Complaints</h2>

            <input
                placeholder="Enter Roll Number"
                value={rollNo}
                onChange={(e) => setRollNo(e.target.value)}
            />

            <button onClick={showComplaints}>
                Show
            </button>

            {error && <p className="error">{error}</p>}

            {complaints.map((complaint) => (
                <div key={complaint.id} className="complaint-card">

                    <h3>Complaint #{complaint.id}</h3>

                    <p>Room: {complaint.room_no}</p>
                    <p>Category: {complaint.category}</p>
                    <p>Description: {complaint.description}</p>
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

            {selectedComplaint && (
    <div className="complaint-card">
        <h3>Complaint Updates</h3>

        {(selectedComplaint.updates || []).length === 0 && (
            <p>No updates yet.</p>
        )}

        {(selectedComplaint.updates || []).map((update) => (
            <p key={update.id}>
                {update.status}: {update.note}
            </p>
        ))}
    </div>
)}
        </div>
    );
}

export default MyComplaints;

