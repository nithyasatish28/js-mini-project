import { useState, useEffect } from "react";
import { API_URL } from "../api";

function WardenDashboard({ refreshKey }) {
    const [complaints, setComplaints] = useState([]);
    const [counts, setCounts] = useState({});
    const [status, setStatus] = useState("");
    const [category, setCategory] = useState("");
    const [notes, setNotes] = useState({});

    async function loadData() {
        const res1 = await fetch(`${API_URL}/complaints`);
        const res2 = await fetch(`${API_URL}/complaints/counts`);
        setComplaints(await res1.json());
        setCounts(await res2.json());
    }
    useEffect(() => {
        loadData();
    }, [refreshKey]);

    async function updateStatus(c) {
        const next = c.status === "open" ? "in_progress" : "resolved";
        const note = notes[c.id] || "";
        await fetch(`${API_URL}/complaints/${c.id}/status?status=${next}&note=${(note)}`,
        { method: "PATCH" });
        setNotes({ ...notes, [c.id]: "" });
        loadData();
    }

    const filtered = complaints.filter(c =>
        (!status || c.status === status) &&
        (!category || c.category === category)
    );
     return (
     <div className="dashboard-card">
        <h2>Warden Dashboard</h2>
        <h3>Complaint Summary</h3>
        <p>Open: {counts.open || 0}</p>
        <p>In Progress: {counts.in_progress || 0}</p>
        <p>Resolved: {counts.resolved || 0}</p>
        <select value={status} onChange={e => setStatus(e.target.value)}>
            <option value="">All Status</option>
            <option value="open">Open</option>
            <option value="in_progress">In Progress</option>
            <option value="resolved">Resolved</option>
            </select>
            
            <select value={category} onChange={e => setCategory(e.target.value)}>
                <option value="">All Categories</option>
                {["electrical", "plumbing", "furniture", "cleaning", "internet"].map(c =><option key={c} value={c}>{c}</option>)}
                
                </select>
                <h3>All Complaints</h3>
                {filtered.map(c => (
                    <div key={c.id} className="complaint-card">
                    <h3>Complaint {c.id}</h3>
                    <p>Roll No: {c.roll_no}</p>
                    <p>Room: {c.room_no}</p>
                    <p>Category: {c.category}</p>
                    <p>Description: {c.description}</p>
                    <p>Status: {c.status}</p>
                    {c.status !== "resolved" && (
                        <>
                        <textarea
                        placeholder="Enter update note"
                        value={notes[c.id] || ""}
                        onChange={e => setNotes({ ...notes, [c.id]: e.target.value })}
                        />
                        <button onClick={() => updateStatus(c)}>
                        Move to next status
                        </button>
                        </>
                    )}
                </div>
            ))}
        </div>
    );
}

export default WardenDashboard;
