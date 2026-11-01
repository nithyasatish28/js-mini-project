import { useState } from "react";
import { API_URL } from "../api";

function RaiseComplaint({ onComplaintAdded }) {
    const [rollNo, setRollNo] = useState("");
    const [roomNo, setRoomNo] = useState("");
    const [category, setCategory] = useState("");
    const [description, setDescription] = useState("");
    const [message, setMessage] = useState("");
    
async function submitComplaint(e) {
    e.preventDefault();
    
    try {
    const response = await fetch(`${API_URL}/complaints?roll_no=${rollNo}&room_no=${roomNo}
        &category=${category}&description=${(description)}`,
                { method: "POST" });
                
    const data = await response.json();
    if (response.ok) {setMessage("Complaint submitted successfully!");
        setRollNo("");
        setRoomNo("");
        setCategory("");
        setDescription("");
        onComplaintAdded();
        } else {
            setMessage(data.detail);}
        } catch {
            setMessage("Unable to connect to server");
        }}
        
        return (
        <div className="dashboard-card">
            <h2>Raise a Complaint</h2>
            <form onSubmit={submitComplaint}>
                <input placeholder="Roll Number" type="number" value={rollNo} onChange={e => setRollNo(e.target.value)} required />
                <input placeholder="Room Number" type="number" value={roomNo} onChange={e => setRoomNo(e.target.value)} required />
                <select value={category} onChange={e => setCategory(e.target.value)} required>
                    <option value="">Select Category</option>
                    {["electrical", "plumbing", "furniture", "cleaning", "internet"].map(c => (
                        <option value={c} key={c}>{c}</option>
                    ))}
                </select>
                <textarea placeholder="Describe your complaint" value={description} onChange={e => setDescription(e.target.value)} minLength={10} required />
                <button type="submit">Submit Complaint</button>
            </form>
            {message && <p>{message}</p>}
        </div>
    );
}

export default RaiseComplaint;
