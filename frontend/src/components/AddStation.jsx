
import React from "react";

function AddStation({ apiUrl, onStationAdded }) {
  async function addStation(event) {
    event.preventDefault();

    const station = {
      name: event.target.name.value,
      location: event.target.location.value,
      capacity: Number(event.target.capacity.value),
      umbrellas_available: Number(event.target.umbrellas_available.value)
    };

    try {
      const response = await fetch(`${apiUrl}/stations`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(station)
      });

      const data = await response.json();

      if (!response.ok) {
        alert(data.detail);
        return;
      }

      alert("Station added successfully!");

      event.target.reset();
      onStationAdded();

    } catch (error) {
      alert("Unable to connect to the server.");
    }
  }

  return (
    <form onSubmit={addStation}>
      <h2>Add Station</h2>

      <input
        name="name"
        placeholder="Station name"
        required
      />

      <input
        name="location"
        placeholder="Location"
        required
      />

      <input
        name="capacity"
        type="number"
        placeholder="Capacity"
        min="1"
        max="30"
        required
      />

      <input
        name="umbrellas_available"
        type="number"
        placeholder="Umbrellas"
        min="0"
        required
      />

      <button type="submit">Add Station</button>
    </form>
  );
}

export default AddStation;
