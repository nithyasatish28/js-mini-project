function StationItem({ station, onBorrow, onDetails }) {
    let emptyLabel = "";
    let fullLabel = "";
    
    if (station.Umbrellas_available === 0){
    emptyLabel = "Empty";}
    else{
    emptyLabel = "";
  }
  
    if (station.free_slots === 0) {
    fullLabel = "Full";}
    else {
    fullLabel = "";
  }

  return (
    <li>
      <h3>{station.name}</h3>
      <p>{station.location}</p>
      <p>{station.umbrellas_available}</p>
      <p>{station.free_slots}</p>
      <p>{emptyLabel}</p>
      <p>{fullLabel}</p>
      <button onClick={() => onBorrow(station.id)}>Borrow</button>
      <button onClick={() => onDetails(station.id)}>Details</button>
    </li>
  );
}

export default StationItem;
