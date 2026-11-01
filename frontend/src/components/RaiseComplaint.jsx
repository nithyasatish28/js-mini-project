import { useState } from "react";

function RaiseComplaint({ API_URL, onAction }) {
  const [rollNo, setRollNo] = useState("");
  const [roomNo, setRoomNo] = useState("");
  const [category, setCategory] = useState("");
  const [description, setDescription] = useState("");

  function addComplaint() {
    fetch(`${API_URL}/complaints?rollno=${rollNo}&roomno=${roomNo}&category=${category}&description=${description}`, {
      method: "POST"
    })
      .then((res) => res.json())  
      .then(() => {
        setRollNo("");
        setRoomNo("");
        setCategory("");
        setDescription("");
        onAction();
      });
  }

  return (
    <div className="card">
      <h2>Raise a Complaint</h2>

      <div>
        <label htmlFor="rollno">Roll Number</label>
        <input id="rollno" type="text" value={rollNo} onChange={(event) => setRollNo(event.target.value)} required/>

        <label htmlFor="roomno">Room Number</label>
        <input id="roomno" type="number" value={roomNo} onChange={(event) => setRoomNo(event.target.value)} required/>

        <label>Category: <strong>{category}</strong></label>
        <div className="button-group">
          <button type="button" onClick={() => setCategory("electrical")}> Electrical </button>
          <button type="button" onClick={() => setCategory("plumbing")}> Plumbing </button>
          <button type="button" onClick={() => setCategory("furniture")}> Furniture </button>
          <button type="button" onClick={() => setCategory("cleaning")}> Cleaning </button>
          <button type="button" onClick={() => setCategory("internet")}> Internet </button>
        </div>

        <label htmlFor="description">Description</label>
        <textarea
          id="description"
          rows="3"
          value={description}
          onChange={(event) => setDescription(event.target.value)}
          required/>

        <button type="button" onClick={addComplaint}>Submit Complaint</button>
      </div>
    </div>
  );
}

export default RaiseComplaint;
