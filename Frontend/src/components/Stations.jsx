import { useState } from "react";

export default function Stations({ stations, onSelectStation, onNeedsAttention, onResetFilter, onBorrow, isFiltered }) {
  const [rolls, setRolls] = useState({});

  return (
    <div>
      <div>
        <h2>Stations</h2>
        {isFiltered && <button onClick={onResetFilter}>Show All</button>}
        <button onClick={onNeedsAttention}>Needs Attention</button>
      </div>

      <ul>
        {stations.map((s) => {
          const free = s.capacity - s.umbrellas_available;
          return (
            <li key={s.id} onClick={() => onSelectStation(s)}>
              <h3>{s.name} ({s.location})</h3>
              <p>Umbrellas: {s.umbrellas_available} | Free: {free}</p>
              {s.umbrellas_available === 0 && <b>[Empty] </b>}
              {free === 0 && <b>[Full]</b>}

              <div onClick={(e) => e.stopPropagation()}>
                <input
                  placeholder="Roll No"
                  value={rolls[s.id] || ""}
                  onChange={(e) => setRolls({ ...rolls, [s.id]: e.target.value })}
                />
                <button onClick={() => { onBorrow(s.id, rolls[s.id]); setRolls({ ...rolls, [s.id]: "" }); }}>
                  Borrow
                </button>
              </div>
            </li>
          );
        })}
      </ul>
    </div>
  );
}