import { useState } from "react";

function RaiseComplaint({ apiUrl, onDone }) {
  const [roll_no, setRollNo] = useState("");
  const [room_no, setRoomNo] = useState("");
  const [category, setCategory] = useState("electrical");
  const [description, setDescription] = useState("");
  const [message, setMessage] = useState("");

  function submitComplaint(event) {
    event.preventDefault();

    const url =
      apiUrl +
      "/complaints?rollno=" + encodeURIComponent(roll_no) +
      "&roomno=" + encodeURIComponent(room_no) +
      "&category=" + encodeURIComponent(category) +
      "&description=" + encodeURIComponent(description);

    fetch(url, { method: "POST" })
      .then((response) => response.json().then((data) => ({ ok: response.ok, data })))
      .then((result) => {
        if (result.ok) {
          setMessage("Complaint submitted!");
          setRollNo("");
          setRoomNo("");
          setDescription("");
          onDone();
        } else {
          setMessage(result.data.detail);
        }
      });
  }

  return (
    <div>
      <h2>Raise a Complaint</h2>

      <form onSubmit={submitComplaint}>
        <input placeholder="Roll number" value={roll_no}
          onChange={(e) => setRollNo(e.target.value)} />

        <input placeholder="Room number" value={room_no}
          onChange={(e) => setRoomNo(e.target.value)} />

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
          onChange={(e) => setDescription(e.target.value)} />

        <button type="submit">Submit</button>
      </form>

      <p>{message}</p>
    </div>
  );
}

export default RaiseComplaint;