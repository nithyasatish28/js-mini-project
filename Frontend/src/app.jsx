import { useState, useEffect } from "react";
import Stations from "./components/Stations";
import AddStation from "./components/AddStation";
import MyUmbrella from "./components/MyUmbrella";

const API_URL = "http://127.0.0.1:8000";

export default function App() {
  const [stations, setStations] = useState([]);
  const [selected, setSelected] = useState(null);
  const [error, setError] = useState("");
  const [filtered, setFiltered] = useState(false);

  // Sync state data from real SQLite backend
  async function fetchStations() {
    try {
      const targetEndpoint = filtered ? `${API_URL}/stations/attention` : `${API_URL}/stations`;
      const res = await fetch(targetEndpoint);
      if (!res.ok) throw new Error("Could not pull network stations map.");
      const data = await res.json();
      setStations(data);
    } catch (err) {
      setError(err.message);
    }
  }

  useEffect(() => {
    fetchStations();
  }, [filtered]);

  // Handle borrow operation
  async function handleBorrow(stationId, rollNo) {
    if (!rollNo?.trim()) return setError("Please enter a roll number.");
    setError("");
    try {
      const res = await fetch(`${API_URL}/borrows?roll_no=${encodeURIComponent(rollNo)}&station_id=${stationId}`, {
        method: "POST"
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Borrow failed");
      fetchStations();
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <div style={{ padding: "20px", fontFamily: "sans-serif" }}>
      <h1>Campus Umbrella Sharing</h1>
      
      {error && (
        <div style={{ color: "white", background: "#d9534f", padding: "10px", borderRadius: "4px", marginBottom: "15px" }}>
          <strong>Notification:</strong> {error}
          <button onClick={() => setError("")} style={{ float: "right", background: "none", color: "white", border: "none", cursor: "pointer" }}>✕</button>
        </div>
      )}

      {/* Part 1: Stations */}
      <Stations
        stations={stations}
        onSelectStation={setSelected}
        onNeedsAttention={() => setFiltered(true)}
        onResetFilter={() => setFiltered(false)}
        onBorrow={handleBorrow}
        isFiltered={filtered}
      />

      {selected && (
        <div style={{ marginTop: "15px", background: "#f9f9f9", padding: "10px", border: "1px solid #ddd" }}>
          <h3>{selected.name} Details</h3>
          <p>Loc: {selected.location} | Cap: {selected.capacity} | Umbrellas: {selected.umbrellas_available} | Free Slots: {selected.capacity - selected.umbrellas_available}</p>
          <button onClick={() => setSelected(null)}>Close Info Panel</button>
        </div>
      )}

      {/* Part 2: My Umbrella (Using your exact prop handlers) */}
      <MyUmbrella 
        stations={stations} 
        apiUrl={API_URL} 
        onError={setError} 
        onSuccess={fetchStations} 
      />

      {/* Part 3: Add Station */}
      <AddStation 
        apiUrl={API_URL} 
        onStationAdded={fetchStations} 
        onError={setError} 
      />
    </div>
  );
}
