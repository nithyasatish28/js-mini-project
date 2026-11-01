function EquipmentItem({ equipment, onBook, onChangeStatus }) {
  return (
    <li className="equipment">
      <h2>{equipment.name}</h2>
      <p>{equipment.type}</p>
      <p>{equipment.lab_room}</p>
      {!equipment.in_service && <p>Out of service</p>}
      <button
        disabled={!equipment.in_service}
        onClick={() => onBook(equipment.id)}
      >
        Book
      </button>
      {" "}
      <button
        onClick={() =>
          onChangeStatus(equipment.id, !Boolean(equipment.in_service))
        }
      >
        {equipment.in_service ? "Out of service" : "In service"}
      </button>
    </li>
  );
}

export default EquipmentItem;
