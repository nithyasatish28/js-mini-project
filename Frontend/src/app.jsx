import { useState, useEffect } from "react";
import Stations from "./components/Stations";
import AddStation from "./components/AddStation";

const API_URL = "http://127.0.0.1:8000";

export default function App() {
  const [stations, setStations] = useState([]);
  const [selected, setSelected] = useState(null);
  const [error, setError] = useState("");
  const [filtered, setFiltered] = useState(false);

  // My Umbrella states
  const [myRollNo, setMyRollNo] = useState("");
  const [activeBorrow, setActiveBorrow] = useState(null);
  const [returnStationId, setReturnStationId] = useState("");

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

  // Real-time backend connection updates
  async function handleBorrow(stationId, rollNo) {
    if (!rollNo?.trim()) return setError("Please enter a roll number.");
    setError("");
    try {
      const res = await fetch(`${API_URL}/borrows?roll_no=${encodeURIComponent(rollNo)}&station_id=${stationId}`, {
        method: "POST"
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Borrow failed");
      
      fetchStations(); // Instantly update view without reloading page
    } catch (err) {
      setError(err.message);
    }
  }

  // Active student check hook
  async function handleCheckActiveBorrow() {
    if (!myRollNo.trim()) return setError("Please input a valid roll number.");
    setError("");
    try {
      const res = await fetch(`${API_URL}/borrows/active?roll_no=${encodeURIComponent(myRollNo)}`);
      const data = await res.json();
      if (!res.ok) {
        setActiveBorrow(null);
        throw new Error(data.detail || "No active record found.");
      }
      setActiveBorrow(data);
    } catch (err) {
      setError(err.message);
    }
  }

  // Active return transaction drop-off hook
  async function handleReturn() {
    if (!returnStationId) return setError("Please choose a dropoff point.");
    setError("");
    try {
      const res = await fetch(`${API_URL}/borrows/${encodeURIComponent(myRollNo)}/return?station_id=${returnStationId}`, {
        method: "PATCH"
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Return validation failure.");
      
      setActiveBorrow(null);
      setReturnStationId("");
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

      {/* Stations Component */}
      <Stations
        stations={stations}
        onSelectStation={setSelected}
        onNeedsAttention={() => setFiltered(true)}
        onResetFilter={() => setFiltered(false)}
        onBorrow={handleBorrow}
        isFiltered={filtered}
      />

      {/* Selected Station Inspection Panel */}
      {selected && (
        <div style={{ marginTop: "15px", background: "#f9f9f9", padding: "10px", border: "1px solid #ddd" }}>
          <h3>{selected.name} Details</h3>
          <p>Loc: {selected.location} | Cap: {selected.capacity} | Umbrellas: {selected.umbrellas_available} | Free Slots: {selected.capacity - selected.umbrellas_available}</p>
          <button onClick={() => setSelected(null)}>Close Info Panel</button>
        </div>
      )}

      {/* Part 2: My Umbrella Panel */}
      <div style={{ border: "1px solid #ccc", padding: "15px", marginTop: "20px", borderRadius: "6px" }}>
        <h3>My Umbrella Status</h3>
        <input 
          type="text" 
          placeholder="Type roll number..." 
          value={myRollNo} 
          onChange={(e) => setMyRollNo(e.target.value)} 
        />
        <button onClick={handleCheckActiveBorrow} style={{ marginLeft: "5px" }}>Show Active Rental</button>

        {activeBorrow && (
          <div style={{ marginTop: "10px", padding: "10px", backgroundColor: "#eef" }}>
            <p>🎒 Student Roll: <b>{activeBorrow.roll_no}</b></p>
            <p>🛫 Origin Point: <b>{activeBorrow.from_station_name}</b></p>
            
            <label style={{ display: "block", marginTop: "10px" }}>Dropoff Point Selection:</label>
            <select value={returnStationId} onChange={(e) => setReturnStationId(e.target.value)}>
              <option value="">-- Choose Dropoff Point --</option>
              {stations.map((s) => (
                <option key={s.id || s.station_id} value={s.id || s.station_id}>
                  {s.name} (Free slots: {s.free_slots})
                </option>
              ))}
            </select>
            <button onClick={handleReturn} style={{ marginLeft: "5px" }}>Process Return</button>
          </div>
        )}
      </div>

      {/* Part 3: Add Station Component Form */}
      <AddStation API_URL={API_URL} onStationAdded={fetchStations} onError={setError} />
    </div>
  );
}
