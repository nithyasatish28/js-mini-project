import { useState } from "react";
import { apiRequest } from "../services/api";

function AddStation({ onStationAdded }) {
  const [name, setName] = useState("");
  const [location, setLocation] = useState("");
  const [capacity, setCapacity] = useState("");
  const [umbrellas, setUmbrellas] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState(false);

  async function handleSubmit(event) {
    event.preventDefault();

    setMessage("");
    setError(false);

    const stationCapacity = Number(capacity);
    const availableUmbrellas = Number(umbrellas);

    if (
      stationCapacity < 1 ||
      stationCapacity > 30 ||
      availableUmbrellas < 0 ||
      availableUmbrellas > stationCapacity
    ) {
      setError(true);
      setMessage(
        "Capacity must be 1–30, and umbrellas cannot exceed capacity."
      );
      return;
    }

    try {
      await apiRequest("/stations", "POST", {
        name: name.trim(),
        location: location.trim(),
        capacity: stationCapacity,
        umbrellas_available: availableUmbrellas
      });

      setMessage("Station added successfully!");

      setName("");
      setLocation("");
      setCapacity("");
      setUmbrellas("");

      onStationAdded();
    } catch (err) {
      setError(true);
      setMessage(err.message);
    }
  }

  return (
    <section className="form-section" id="add-station">
      <h2>Add a Station</h2>

      <form onSubmit={handleSubmit}>
        <label>Station Name</label>

        <input
          type="text"
          placeholder="Example: Hostel"
          value={name}
          onChange={(event) => setName(event.target.value)}
          required
        />

        <label>Location</label>

        <input
          type="text"
          placeholder="Example: Ground floor"
          value={location}
          onChange={(event) => setLocation(event.target.value)}
          required
        />

        <label>Station Capacity</label>

        <input
          type="number"
          min="1"
          max="30"
          value={capacity}
          onChange={(event) => setCapacity(event.target.value)}
          required
        />

        <label>Umbrellas Available</label>

        <input
          type="number"
          min="0"
          value={umbrellas}
          onChange={(event) => setUmbrellas(event.target.value)}
          required
        />

        <button type="submit">Add Station</button>
      </form>

      {message && (
        <p className={error ? "error" : "success"}>
          {message}
        </p>
      )}
    </section>
  );
}

export default AddStation;