
import { useState } from "react";

const API_URL = "http://127.0.0.1:8001";

function AddStation({ onAdd }) {
  const [name, setName] = useState("");
  const [location, setLocation] = useState("");
  const [capacity, setCapacity] = useState("");
  const [umbrellas, setUmbrellas] = useState("");
  const [message, setMessage] = useState("");

  function addStation() {
    if (name === "" || location === "") {
      setMessage("Please enter station name and location");
      return;
    }

    if (capacity === "" || umbrellas === "") {
      setMessage("Please enter capacity and available umbrellas");
      return;
    }

    if (capacity < 1 || capacity > 30) {
      setMessage("Capacity must be between 1 and 30");
      return;
    }

    if (umbrellas < 0) {
      setMessage("Available umbrellas cannot be negative");
      return;
    }

    if (umbrellas > capacity) {
      setMessage("Available umbrellas cannot exceed capacity");
      return;
    }

    fetch(`${API_URL}/stations?name=${name}&location=${location}&capacity=${capacity}&umbrellas_available=${umbrellas}`, {
      method: "POST"
    })
      .then(async (response) => {
        const data = await response.json();

        if (!response.ok) {
          setMessage(data.detail);
          return;
        }

        setMessage("Station added successfully");
        onAdd();
      })
      .catch((error) => {
        setMessage("Unable to connect to the server");
        console.log("Fetch error:", error);
      });
  }

  return (
    <>
      <h2>Add Station</h2>
      <input placeholder="Station name" onChange={(e) => setName(e.target.value)} />
      <input placeholder="Location" onChange={(e) => setLocation(e.target.value)} />
      <input placeholder="Capacity" onChange={(e) => setCapacity(e.target.value)} />
      <input placeholder="Available umbrellas" onChange={(e) => setUmbrellas(e.target.value)} />
      <button onClick={addStation}>Add Station</button>
      <p>{message}</p>
    </>
  );
}

export default AddStation;

