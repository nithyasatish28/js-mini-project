import { useState } from "react";

function AddEquipment({ API_URL, onEquipmentAdded }) {
const [name, setName] = useState("");
const [equipmentType, setEquipmentType] = useState("");
const [labRoom, setLabRoom] = useState("");
const [message, setMessage] = useState("");

// E3 - Add equipment
function addEquipment() {
if (name === "") {
setMessage("Enter equipment name");
return;
}


if (equipmentType === "") {
  setMessage("Enter equipment type");
  return;
}

if (labRoom === "") {
  setMessage("Enter lab room");
  return;
}

fetch(
  API_URL + "/equipment?name=" + name +
  "&equipment_type=" + equipmentType +
  "&lab_room=" + labRoom,
  {
    method: "POST"
  }
)
  .then((response) => response.json())
  .then(() => {
    setMessage("Equipment added successfully");

    setName("");
    setEquipmentType("");
    setLabRoom("");

    onEquipmentAdded();
  });


}

return ( <div> <h2>Add Equipment</h2>


  <p>Equipment name</p>
  <input
    type="text"
    value={name}
    onChange={(event) => setName(event.target.value)}
  />

  <p>Equipment type</p>
  <input
    type="text"
    value={equipmentType}
    onChange={(event) => setEquipmentType(event.target.value)}
  />

  <p>Lab room</p>
  <input
    type="text"
    value={labRoom}
    onChange={(event) => setLabRoom(event.target.value)}
  />

  <p>
    <button onClick={addEquipment}>Add Equipment</button>
  </p>

  <p>{message}</p>
</div>


);
}

export default AddEquipment;