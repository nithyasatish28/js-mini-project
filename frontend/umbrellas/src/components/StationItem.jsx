function StationItem({ station, onAdd }) {
  return (
    <li className="station">
      <h2>{station.name}</h2>
      <p>{station.location}</p>
      <p>Capacity: {station.capacity}</p>
      <p>Umbrellas available: {station.umbrellas_available}</p>
      <p>Free slots: {station.free_slots}</p>
      {station.umbrellas_available > 0 ? (
        <button onClick={() => onAdd(station.id)}>Borrow</button>
      ) : (
        <p>No umbrellas available</p>
      )}
    </li>
  );
}

export default StationItem;