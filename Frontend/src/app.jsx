import { useState } from "react";
import Stations from "./components/Stations";

const initial = [
  { id: 1, name: "Library", location: "Main Block", capacity: 10, umbrellas_available: 5 },
  { id: 2, name: "Cafeteria", location: "Food Court", capacity: 8, umbrellas_available: 0 },
  { id: 3, name: "Sports Complex", location: "Grounds", capacity: 5, umbrellas_available: 5 },
  { id: 4, name: "Hostel A", location: "Residential Zone", capacity: 12, umbrellas_available: 4 },
];

export default function App() {
  const [stations, setStations] = useState(initial);
  const [selected, setSelected] = useState(null);
  const [error, setError] = useState("");
  const [filtered, setFiltered] = useState(false);

  function handleBorrow(id, roll) {
    if (!roll?.trim()) return setError("Please enter a roll number.");
    setError("");
    setStations((prev) =>
      prev.map((s) => (s.id === id ? (s.umbrellas_available ? { ...s, umbrellas_available: s.umbrellas_available - 1 } : (setError("Station empty!"), s)) : s))
    );
  }

  return (
    <div>
      <h1>Campus Umbrella Sharing</h1>
      {error && <p>{error}</p>}

      <Stations
        stations={stations}
        onSelectStation={setSelected}
        onNeedsAttention={() => { setError(""); setStations(initial.filter((s) => !s.umbrellas_available || s.capacity === s.umbrellas_available)); setFiltered(true); }}
        onResetFilter={() => { setError(""); setStations(initial); setFiltered(false); }}
        onBorrow={handleBorrow}
        isFiltered={filtered}
      />

      {selected && (
        <div>
          <h3>{selected.name} Details</h3>
          <p>Loc: {selected.location} | Cap: {selected.capacity} | Umbrellas: {selected.umbrellas_available} | Free: {selected.capacity - selected.umbrellas_available}</p>
          <button onClick={() => setSelected(null)}>Close</button>
        </div>
      )}
    </div>
  );
}