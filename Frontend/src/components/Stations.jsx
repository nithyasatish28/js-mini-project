import { useState } from "react";

export default function Stations({ stations, onSelectStation, onNeedsAttention, onResetFilter, onBorrow, isFiltered }) {
  const [rolls, setRolls] = useState({});

  return (
    <div className="box">
      <h2>Stations</h2>
      
      <div style={{ marginBottom: "15px" }}>
        {isFiltered ? (
          <button onClick={onResetFilter}>Show All Stations</button>
        ) : (
          <button onClick={onNeedsAttention}>Needs Attention</button>
        )}
      </div>

      <div className="grid">
        {stations.map((station) => {
          const freeSlots = station.capacity - station.umbrellas_available;
          const isEmpty = station.umbrellas_available === 0;
          const isFull = freeSlots === 0;

          return (
            <div
              key={station.id}
              className="card"
              onClick={() => onSelectStation(station)}
            >
              <h3>{station.name}</h3>
              <p><b>Location:</b> {station.location}</p>
              <p><b>Umbrellas:</b> {station.umbrellas_available}</p>
              <p><b>Free Slots:</b> {freeSlots}</p>

              {isEmpty && <p style={{ color: "red" }}><b>[Empty]</b></p>}
              {isFull && <p style={{ color: "orange" }}><b>[Full]</b></p>}

              <div onClick={(e) => e.stopPropagation()} style={{ marginTop: "10px" }}>
                <input
                  type="text"
                  placeholder="Roll No"
                  value={rolls[station.id] || ""}
                  onChange={(e) =>
                    setRolls({ ...rolls, [station.id]: e.target.value })
                  }
                  style={{ width: "100px" }}
                />
                <button
                  onClick={() => {
                    onBorrow(station.id, rolls[station.id]);
                    setRolls({ ...rolls, [station.id]: "" });
                  }}
                >
                  Borrow
                </button>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}