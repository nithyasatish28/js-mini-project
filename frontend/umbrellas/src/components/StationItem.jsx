function StationItem({ station, onBorrow, onDetails }) {
    let emptyLabel = "";
    let fullLabel = "";
    
    if (station.umbrellas_available === 0){
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
      <h3>name: {station.name}</h3>
      <p>Location: {station.location}</p>
      <p>Avilability: {station.umbrellas_available}</p>
      <p>free_slots: {station.free_slots}</p>
      <p>emptyLabel: {emptyLabel}</p>
      <p>fullLable: {fullLabel}</p>
      <button onClick={() => onBorrow(station.id)}>Borrow</button>
      <button onClick={() => onDetails(station.id)}>Details</button>
    </li>
  );
}

export default StationItem;
