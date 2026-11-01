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
      <input placeholder="Name" value={name} onChange={(event) => setName(event.target.value)} />
      <input placeholder="Location" value={location} onChange={(event) => setLocation(event.target.value)} />
      <input placeholder="Capacity" value={capacity} onChange={(event) => setCapacity(event.target.value)} />
      <input placeholder="Starting umbrellas" value={umbrellas} onChange={(event) => setUmbrellas(event.target.value)} />
      <button onClick={addStation}>Add</button>
    </>
  );
}

export default AddStation;