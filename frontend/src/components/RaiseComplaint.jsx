import { useState } from "react";
import { API_URL } from "../api";

function RaiseComplaint({ onComplaintAdded }) {
const [rollNo, setRollNo] = useState("");
const [roomNo, setRoomNo] = useState("");
const [category, setCategory] = useState("");
const [description, setDescription] = useState("");
const [message, setMessage] = useState("");
const [error, setError] = useState("");

async function submitComplaint(e) {
    e.preventDefault();

    // Check roll number and room number
    if (!/^[1-9]\d*$/.test(rollNo)) {
        setError("Roll number must be a positive whole number");
        setMessage("");
        return;
    }

    if (!/^[1-9]\d*$/.test(roomNo)) {
        setError("Room number must be a positive whole number");
        setMessage("");
        return;
    }

    try {
        const response = await fetch(
            `${API_URL}/complaints?roll_no=${encodeURIComponent(rollNo)}&room_no=${encodeURIComponent(roomNo)}&category=${encodeURIComponent(category)}&description=${encodeURIComponent(description)}`,
            {
                method: "POST"
            }
        );

        const data = await response.json();

        if (response.ok) {
            setMessage("Complaint submitted successfully!");
            setError("");

            setRollNo("");
            setRoomNo("");
            setCategory("");
            setDescription("");

            onComplaintAdded();
        } else {
            setError(data.detail);
            setMessage("");
        }
    } catch (error) {
        setError("Unable to connect to the server. Please try again.");
        setMessage("");
    }
}

return (
    <div className="dashboard-card">
        <h2>Raise a Complaint</h2>

        <form onSubmit={submitComplaint}>

            <input
                type="number"
                placeholder="Roll Number"
                value={rollNo}
                onChange={(e) => setRollNo(e.target.value)}
                min="1"
                step="1"
                required
            />

            <input
                type="number"
                placeholder="Room Number"
                value={roomNo}
                onChange={(e) => setRoomNo(e.target.value)}
                min="1"
                step="1"
                required
            />

            <select
                value={category}
                onChange={(e) => setCategory(e.target.value)}
                required
            >
                <option value="">Select Category</option>
                <option value="electrical">Electrical</option>
                <option value="plumbing">Plumbing</option>
                <option value="furniture">Furniture</option>
                <option value="cleaning">Cleaning</option>
                <option value="internet">Internet</option>
            </select>

            <textarea
                placeholder="Describe your complaint"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                minLength={10}
                required
            />

            <button type="submit">
                Submit Complaint
            </button>

        </form>

        {message && <p>{message}</p>}
        {error && <p className="error">{error}</p>}
    </div>
);

}

export default RaiseComplaint;

