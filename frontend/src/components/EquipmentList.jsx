import EquipmentItem from "./EquipmentItem";

function EquipmentList({ equipments, onBook, onToggleService, onFilter }) {
  return (
    <>
      <h1>Lab Equipment</h1>

      <select onChange={(e) => onFilter(e.target.value)}>
        <option value="">All Equipment</option>
        <option value="microscope">Microscope</option>
        <option value="oscilloscope">Oscilloscope</option>
        <option value="3d-printer">3D Printer</option>
        <option value="laptop">Laptop</option>
        <option value="camera">Camera</option>
      </select>

      <ul className="products">
        {equipments.map((equipment) => (
          <EquipmentItem
            key={equipment.id}
            equipment={equipment}
            onBook={onBook}
            onToggleService={onToggleService}
          />
        ))}
      </ul>
    </>
  );
}

export default EquipmentList;