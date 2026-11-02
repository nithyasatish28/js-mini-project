import { useState } from "react";
function AddStation({ API_URL, handleResult }) {
  const [name, setName] = useState("");
  const [location, setLocation] = useState("");
  const [capacity, setCapacity] = useState("");
  const [umbrellas, setUmbrellas] = useState("");
  function addStation() {
    fetch(
      API_URL + "/stations?name=" + name + "&location=" + location +
        "&capacity=" + capacity + "&umbrellas_available=" + umbrellas,
      { method: "POST" }
    )
      .then((response) => response.json())
      .then((data) => handleResult(data, "Station added"));
  }
  return (
    <>
      <h2>Add a station</h2>
      <input placeholder="Name" value={name} onChange={(n) => setName(n.target.value)} />
      <input placeholder="Location" value={location} onChange={(l) => setLocation(l.target.value)} />
      <input placeholder="capacity" value={capacity} onChange={(c) => setCapacity(c.target.value)} />
      <input placeholder="AvailabilityToBorrow" value={umbrellas} onChange={(a) => setUmbrellas(a.target.value)} />
      <button onClick={addStation}>Add</button>
    </>
  );
}
export default AddStation;
