function StationItem({ station }) {
  return (
    <div className="card">
      <h3>{station.name}</h3>
      <p>Location: {station.location}</p>
      <p>Umbrellas: {station.umbrellas_available}</p>
      <p>Free slots: {station.free_slots}</p>
    </div>
  );
}

export default StationItem;