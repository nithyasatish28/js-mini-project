import EquipmentItem from "./EquipmentItem";

function EquipmentList({
  equipment,
  onBook,
  onChangeService,
  onFilter,
  loading
}) {

  return (
    <section className="section">

      <div className="section-heading">
        <div>
          <h2>Available Equipment</h2>
          <p>Browse and book laboratory equipment</p>
        </div>

        <select
          className="filter-select"
          onChange={(e) => onFilter(e.target.value)}
        >
          <option value="">All Equipment</option>
          <option value="microscope">Microscope</option>
          <option value="oscilloscope">Oscilloscope</option>
          <option value="3d-printer">3D Printer</option>
          <option value="laptop">Laptop</option>
          <option value="camera">Camera</option>
        </select>
      </div>

      {loading && <p>Loading equipment...</p>}

      <div className="equipment-list">

        {equipment.map((item) => (
          <EquipmentItem
            key={item.id}
            item={item}
            onBook={onBook}
            onChangeService={onChangeService}
          />
        ))}

        {!loading && equipment.length === 0 && (
          <p>No equipment found.</p>
        )}

      </div>

    </section>
  );
}

export default EquipmentList;