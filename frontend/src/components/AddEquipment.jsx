import { useState } from "react";

function AddEquipment({ onAdd }) {

  const [name, setName] = useState("");
  const [type, setType] = useState("microscope");
  const [labRoom, setLabRoom] = useState("");

  async function handleSubmit(e) {
    e.preventDefault();

    if (!name.trim() || !labRoom.trim()) {
      alert("Please fill in all fields.");
      return;
    }

    const success = await onAdd(name.trim(), type, labRoom.trim());

    if (success) {
      setName("");
      setType("microscope");
      setLabRoom("");
    }
  }

  return (
    <section className="section">

      <h2>Add Equipment</h2>
      <p>Add a new item to the laboratory inventory.</p>

      <form className="add-form" onSubmit={handleSubmit}>

        <input
          type="text"
          placeholder="Equipment name"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />

        <select
          value={type}
          onChange={(e) => setType(e.target.value)}
        >
          <option value="microscope">Microscope</option>
          <option value="oscilloscope">Oscilloscope</option>
          <option value="3d-printer">3D Printer</option>
          <option value="laptop">Laptop</option>
          <option value="camera">Camera</option>
        </select>

        <input
          type="text"
          placeholder="Lab room"
          value={labRoom}
          onChange={(e) => setLabRoom(e.target.value)}
        />

        <button type="submit" className="primary-btn">
          Add Equipment
        </button>

      </form>

    </section>
  );
}

export default AddEquipment;
