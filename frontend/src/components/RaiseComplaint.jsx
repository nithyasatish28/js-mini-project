import { useState } from "react";

const API_URL = "http://127.0.0.1:8001";

function RaiseComplaint() {
  const [roll_no, setRollNo] = useState("");
  const [room_no, setRoomNo] = useState("");
  const [category, setCategory] = useState("electrical");
  const [description, setDescription] = useState("");
  const [message, setMessage] = useState("");

  function submitComplaint(event) {
    event.preventDefault();

    fetch(API_URL + "/complaints", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        roll_no,
        room_no,
        category,
        description
      })
    })
      .then((response) => {
        if (response.ok) {
          setMessage("Complaint submitted!");
          setRollNo("");
          setRoomNo("");
          setDescription("");
        } else {
          setMessage("Failed to submit complaint.");
        }
      });
  }

  return (
    <div>
      <h2>Raise a Complaint</h2>

      <form onSubmit={submitComplaint}>
        <input placeholder="Roll number" value={roll_no}
          onChange={(e) => setRollNo(e.target.value)} required />

        <input placeholder="Room number" value={room_no}
          onChange={(e) => setRoomNo(e.target.value)} required />

        <select value={category}
          onChange={(e) => setCategory(e.target.value)}>
          <option value="electrical">Electrical</option>
          <option value="plumbing">Plumbing</option>
          <option value="furniture">Furniture</option>
          <option value="cleaning">Cleaning</option>
          <option value="internet">Internet</option>
        </select>

        <textarea placeholder="Describe your complaint (at least 10 characters)"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          minLength={10} required />

        <button type="submit">Submit</button>
      </form>

      <p>{message}</p>
    </div>
  );
}

export default RaiseComplaint;