import { useState } from "react";

const TYPES = ["microscope", "oscilloscope", "3d-printer", "laptop", "camera"];

function AddEquipment({ apiUrl, onRefresh }) {
  const [name, setName] = useState("");
  const [type, setType] = useState(TYPES[0]);
  const [labRoom, setLabRoom] = useState("");
  const [error, setError] = useState("");
  const [msg, setMsg] = useState("");

  function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setMsg("");
    if (!name || !labRoom) {
      setError("Name and lab room are required.");
      return;
    }
    fetch(
      `${apiUrl}/equipments?name=${encodeURIComponent(name)}&type=${type}&lab_room=${encodeURIComponent(labRoom)}`,
      { method: "POST" }
    )
      .then((res) => res.json())
      .then((data) => {
        if (data.detail) {
          setError(data.detail);
        } else {
          setMsg(`"${data.name}" added!`);
          setName("");
          setType(TYPES[0]);
          setLabRoom("");
          onRefresh();
        }
      });
  }

  return (
    <>
      <h2>Add Equipment</h2>
      <form className="add-form" onSubmit={handleSubmit}>
        <div>
          <label>Name</label>
          <input
            type="text"
            placeholder="e.g. Canon DSLR"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
        </div>
        <div>
          <label>Type</label>
          <select value={type} onChange={(e) => setType(e.target.value)}>
            {TYPES.map((t) => (
              <option key={t} value={t}>{t}</option>
            ))}
          </select>
        </div>
        <div>
          <label>Lab Room</label>
          <input
            type="text"
            placeholder="e.g. Lab 101"
            value={labRoom}
            onChange={(e) => setLabRoom(e.target.value)}
          />
        </div>
        <button type="submit" className="btn-primary">Add Equipment</button>
      </form>

      {error && <p className="error">{error}</p>}
      {msg && <p className="success">{msg}</p>}
    </>
  );
}

export default AddEquipment;