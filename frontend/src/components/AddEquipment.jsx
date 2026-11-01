import { useState } from "react";

function AddEquipment({ onAdd }) {

  const [name, setName] = useState("");
  const [equipmentType, setEquipmentType] = useState("");
  const [labRoom, setLabRoom] = useState("");

  function handleAdd(e) {
    e.preventDefault();

    onAdd(name, equipmentType, labRoom);
  }

  return (
    <>
      <h1>Add Equipment</h1>

      <form onSubmit={handleAdd}>

        <input
          type="text"
          placeholder="Equipment Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />

        <select
          value={equipmentType}
          onChange={(e) => setEquipmentType(e.target.value)}
        >
          <option value="">Select Type</option>
          <option value="microscope">Microscope</option>
          <option value="oscilloscope">Oscilloscope</option>
          <option value="3d-printer">3D Printer</option>
          <option value="laptop">Laptop</option>
          <option value="camera">Camera</option>
        </select>

        <input
          type="text"
          placeholder="Lab Room"
          value={labRoom}
          onChange={(e) => setLabRoom(e.target.value)}
        />

        <button type="submit">
          Add Equipment
        </button>

      </form>
    </>
  );
}

export default AddEquipment;