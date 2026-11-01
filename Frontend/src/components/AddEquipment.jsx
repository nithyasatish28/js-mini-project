import { useState } from "react";

const ALLOWED_EQUIPMENT_TYPES = [
  "microscope",
  "oscilloscope",
  "3d-printer",
  "laptop",
  "camera",
];

function AddEquipment({ API_URL, onEquipmentAdded }) {
  const [name, setName] = useState("");
  const [equipmentType, setEquipmentType] = useState("microscope");
  const [labRoom, setLabRoom] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  // E3 - Add equipment
  function addEquipment() {
    if (name.trim() === "") {
      setError("Enter equipment name");
      setMessage("");
      return;
    }

    if (equipmentType === "") {
      setError("Select equipment type");
      setMessage("");
      return;
    }

    if (labRoom.trim() === "") {
      setError("Enter lab room");
      setMessage("");
      return;
    }

    const query = new URLSearchParams({
      name: name.trim(),
      equipment_type: equipmentType,
      lab_room: labRoom.trim(),
    });

    fetch(`${API_URL}/equipment?${query}`, {
      method: "POST",
    })
      .then(async (response) => {
        const data = await response.json();
        if (!response.ok) {
          throw new Error(data.detail ?? `Request failed (${response.status})`);
        }
        return data;
      })
      .then(() => {
        setMessage("Equipment added successfully.");
        setError("");

        setName("");
        setEquipmentType("microscope");
        setLabRoom("");

        onEquipmentAdded();
      })
      .catch((requestError) => {
        setMessage("");
        setError(requestError.message);
      });
  }

  return (
    <section>
      <h2>Add Equipment</h2>

      <p>
        <label>
          Equipment name{" "}
          <input
            type="text"
            value={name}
            onChange={(event) => setName(event.target.value)}
          />
        </label>
      </p>

      <p>
        <label>
          Equipment type{" "}
          <select
            value={equipmentType}
            onChange={(event) => setEquipmentType(event.target.value)}
          >
            {ALLOWED_EQUIPMENT_TYPES.map((type) => (
              <option key={type} value={type}>
                {type}
              </option>
            ))}
          </select>
        </label>
      </p>

      <p>
        <label>
          Lab room{" "}
          <input
            type="text"
            value={labRoom}
            onChange={(event) => setLabRoom(event.target.value)}
          />
        </label>
      </p>

      <p>
        <button onClick={addEquipment}>Add Equipment</button>
      </p>

      {error && <p role="alert">{error}</p>}
      {message && <p role="status">{message}</p>}
    </section>
  );
}

export default AddEquipment;
