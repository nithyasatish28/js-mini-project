import { useState } from "react";

function RaiseForm({ onAdd }) {
  const [rollNo, setRollNo] = useState("");
  const [roomNo, setRoomNo] = useState("");
  const [category, setCategory] = useState("electrical");
  const [description, setDescription] = useState("");

  return (
    <>
      <h2>Raise a complaint</h2>
      <p>
        Roll number: <input value={rollNo} onChange={(e) => setRollNo(e.target.value)} />
      </p>
      <p>
        Room number: <input value={roomNo} onChange={(e) => setRoomNo(e.target.value)} />
      </p>
            <p>
        Category: <select value={category} onChange={(e) => setCategory(e.target.value)}>
          <option value="electrical">electrical</option>
          <option value="plumbing">plumbing</option>
          <option value="furniture">furniture</option>
          <option value="cleaning">cleaning</option>
          <option value="internet">internet</option>
        </select>
      </p>
      <p>
        Description: <input value={description} onChange={(e) => setDescription(e.target.value)} />
      </p>
      <button onClick={() => onAdd(rollNo, roomNo, category, description)}>Raise complaint</button>
    </>
  );
}

export default RaiseForm;