import { useState } from "react";

export default function AddStation({ apiUrl, onStationAdded, onError }) {
  const [name, setName] = useState("");
  const [location, setLocation] = useState("");
  const [capacity, setCapacity] = useState("");
  const [umbrellas, setUmbrellas] = useState("");

  async function handleSubmit(e) {
    e.preventDefault();
    onError("");

    try {
      const queryParams = new URLSearchParams({
        name,
        location,
        capacity,
        umbrellas_available: umbrellas
      });

      const res = await fetch(`${apiUrl}/stations?${queryParams}`, {
        method: "POST"
      });
      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.detail || "Failed to provision new station.");
      }

      setName("");
      setLocation("");
      setCapacity("");
      setUmbrellas("");
      onStationAdded();
    } catch (err) {
      onError(err.message);
    }
  }

  return (
    <div className="section-block" style={{ border: "1px solid #ccc", padding: "15px", marginTop: "20px", borderRadius: "6px" }}>
      <h2>Add Station</h2>
      <form onSubmit={handleSubmit} style={{ display: "flex", flexDirection: "column", gap: "8px", maxWidth: "300px" }}>
        <input type="text" placeholder="Station Name" value={name} onChange={(e) => setName(e.target.value)} required />
        <input type="text" placeholder="Location Info" value={location} onChange={(e) => setLocation(e.target.value)} required />
        <input type="number" placeholder="Total Capacity (1-30)" value={capacity} onChange={(e) => setCapacity(e.target.value)} required />
        <input type="number" placeholder="Starting Umbrellas" value={umbrellas} onChange={(e) => setUmbrellas(e.target.value)} required />
        <button className="btn-primary" type="submit">Add Station</button>
      </form>
    </div>
  );
}
