import React from "react";

function StationCard({ station, onSelect }) {
  const isEmpty = station.umbrellas_available === 0;

  const isFull =
    station.capacity === station.umbrellas_available;

  return (
    <div
      className="station-card"
      onClick={() => onSelect(station.id)}
    >
      <h3>{station.name}</h3>

      <p>Location: {station.location}</p>

      <p>
        Umbrellas available: {station.umbrellas_available}
      </p>

      <p>
        Free slots: {station.free_slots}
      </p>

      {isEmpty ? (
        <span className="status empty">Empty</span>
      ) : isFull ? (
        <span className="status full">Full</span>
      ) : (
        <span className="status available">Available</span>
      )}
    </div>
  );
}

export default StationCard;