import EquipmentItem from "./EquipmentItem";

function EquipmentList({ equipment, onBook, onChangeStatus }) {
  if (equipment.length === 0) {
    return <p>No equipment found.</p>;
  }

  return (
    <ul className="equipment-list">
      {equipment.map((item) => (
        <EquipmentItem
          key={item.id}
          equipment={item}
          onBook={onBook}
          onChangeStatus={onChangeStatus}
        />
      ))}
    </ul>
  );
}

export default EquipmentList;