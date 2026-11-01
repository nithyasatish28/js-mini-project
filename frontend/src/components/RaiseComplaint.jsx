import { useState } from "react";

function RaiseComplaint({ message, raiseComplaint }) {
  const [rollNo, setRollNo] = useState("");
  const [roomNo, setRoomNo] = useState("");
  const [category, setCategory] = useState("electrical");
  const [description, setDescription] = useState("");

  return (
    <>
      <h2>Raise a complaint</h2>
      <input placeholder="Roll number" value={rollNo} onChange={(e) => setRollNo(e.target.value)} />
      <input placeholder="Room number" value={roomNo} onChange={(e) => setRoomNo(e.target.value)} />
      <select value={category} onChange={(e) => setCategory(e.target.value)}>
        <option value="electrical">electrical</option>
        <option value="plumbing">plumbing</option>
        <option value="furniture">furniture</option>
        <option value="cleaning">cleaning</option>
        <option value="internet">internet</option>
      </select>
      <input placeholder="Description" value={description} onChange={(e) => setDescription(e.target.value)} />
      <button onClick={() => raiseComplaint(rollNo, roomNo, category, description)}>Raise</button>
      <p>{message}</p>
    </>
  );
}

export default RaiseComplaint;