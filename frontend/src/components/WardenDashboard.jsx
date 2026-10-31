import { useState, useEffect } from "react";
import { API_URL } from "../api";

function WardenDashboard({ refreshKey }) {
    const [complaints, setComplaints] = useState([]);
    const [counts, setCounts] = useState({
        open: 0,
        in_progress: 0,
        resolved: 0
    });

    const [status, setStatus] = useState("");
    const [category, setCategory] = useState("");
    const [notes, setNotes] = useState({});
    const [error, setError] = useState("");

    async function getComplaints() {
        const response = await fetch(`${API_URL}/complaints`);
        const data = await response.json();

        if (response.ok) {
            setComplaints(data);
        } else {
            setError(data.detail);
        }
    }

    async function getCounts() {
        const response = await fetch(`${API_URL}/complaints/counts`);
        const data = await response.json();

        if (response.ok) {
            setCounts(data);
        } else {
            setError(data.detail);
        }
    }

    useEffect(() => {
        getComplaints();
        getCounts();
    }, [refreshKey]);

    async function moveToNextStatus(complaint) {
        let nextStatus;

        if (complaint.status === "open") {
            nextStatus = "in_progress";
        } else if (complaint.status === "in_progress") {
            nextStatus = "resolved";
        }

        const note = notes[complaint.id] || "";

        const response = await fetch(
            `${API_URL}/complaints/${complaint.id}/status?status=${nextStatus}&note=${encodeURIComponent(note)}`,
            {
                method: "PATCH"
            }
        );

        const data = await response.json();

        if (response.ok) {
            setError("");
            setNotes({ ...notes, [complaint.id]: "" });
            getComplaints();
            getCounts();
        } else {
            setError(data.detail);
        }
    }

    const filteredComplaints = complaints.filter((complaint) => {
        const matchesStatus =
            status === "" || complaint.status === status;

        const matchesCategory =
            category === "" || complaint.category === category;

        return matchesStatus && matchesCategory;
    });

    return (
    <div className="dashboard-card">
        <h2>Warden Dashboard</h2>

            <h3>Complaint Summary</h3>

            <p>Open: {counts.open}</p>
            <p>In Progress: {counts.in_progress}</p>
            <p>Resolved: {counts.resolved}</p>

            <h3>Filter Complaints</h3>

            <select
                value={status}
                onChange={(e) => setStatus(e.target.value)}
            >
                <option value="">All Status</option>
                <option value="open">Open</option>
                <option value="in_progress">In Progress</option>
                <option value="resolved">Resolved</option>
            </select>

            <select
                value={category}
                onChange={(e) => setCategory(e.target.value)}
            >
                <option value="">All Categories</option>
                <option value="electrical">Electrical</option>
                <option value="plumbing">Plumbing</option>
                <option value="furniture">Furniture</option>
                <option value="cleaning">Cleaning</option>
                <option value="internet">Internet</option>
            </select>

            <h3>All Complaints</h3>

            {error && <p className="error">{error}</p>}

            {filteredComplaints.map((complaint) => (
                <div key={complaint.id} className="complaint-card">

                    <h3>Complaint #{complaint.id}</h3>

                    <p>Roll Number: {complaint.roll_no}</p>
                    <p>Room Number: {complaint.room_no}</p>
                    <p>Category: {complaint.category}</p>
                    <p>Description: {complaint.description}</p>

                    <p className={`status status-${complaint.status}`}>
                        {complaint.status}
                    </p>

                    {complaint.status !== "resolved" && (
                        <div>
                            <textarea
                                placeholder="Enter update note"
                                value={notes[complaint.id] || ""}
                                onChange={(e) =>
                                    setNotes({
                                        ...notes,
                                        [complaint.id]: e.target.value
                                    })
                                }
                            />

                            <button
                                onClick={() => moveToNextStatus(complaint)}
                            >
                                Move to next status
                            </button>
                        </div>
                    )}

                </div>
            ))}
        </div>
    );
}

export default WardenDashboard;

