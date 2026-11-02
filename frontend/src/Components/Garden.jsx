import { useState } from "react";

function Garden({
  plants,
  selectedType,
  onTypeChange,
  onlyNeedsWater,
  onToggleNeedsWater,
  onAdopt,
}) {
  
  const [rollNumbers, setRollNumbers] = useState({});

  function handleRollChange(plantId, value) {
    setRollNumbers({
      ...rollNumbers,
      [plantId]: value,
    });
  }

  function handleAdoptClick(plantId) {
    const rollNo = rollNumbers[plantId] || "";
    onAdopt(plantId, rollNo);
  }

  return (
    <section className="section garden-section">
      <div className="section-header">
        <h2>🌿 Campus Garden</h2>
        <p>Browse campus plants, see who is caring for them, or adopt one yourself.</p>
      </div>

      {/* Filter Toolbar */}
      <div className="toolbar">
        <div className="filter-group">
          <label htmlFor="type-filter"><strong>Filter by Type:</strong></label>
          <select
            id="type-filter"
            value={selectedType}
            onChange={(e) => onTypeChange(e.target.value)}
            className="select-input"
          >
            <option value="">All Types</option>
            <option value="succulent">Succulent</option>
            <option value="flowering">Flowering</option>
            <option value="herb">Herb</option>
            <option value="indoor">Indoor</option>
            <option value="tree">Tree</option>
          </select>
        </div>

        <button
          className={`btn ${onlyNeedsWater ? "btn-active" : "btn-secondary"}`}
          onClick={onToggleNeedsWater}
        >
          {onlyNeedsWater ? "💧 Showing: Needs Water Today" : "💧 Needs Water Today"}
        </button>
      </div>

      {/* Plant Cards Grid */}
      {plants.length === 0 ? (
        <p className="empty-message">No plants found matching the selected filter.</p>
      ) : (
        <div className="plant-grid">
          {plants.map((plant) => (
            <div key={plant.id} className="plant-card">
              <div className="card-top">
                <span className="plant-type-badge">{plant.type}</span>
                {plant.needs_water ? (
                  <span className="badge badge-needs-water">Needs water</span>
                ) : (
                  <span className="badge badge-ok">Watered</span>
                )}
              </div>

              <h3 className="plant-name">{plant.name}</h3>
              <p className="plant-location">📍 {plant.location}</p>
              <p className="plant-frequency">
                Water every <strong>{plant.water_every_days}</strong> days
              </p>

              <p className="plant-watered">
                Last watered:{" "}
                <strong>
                  {plant.last_watered ? plant.last_watered : "Never watered"}
                </strong>
              </p>

              <div className="adoption-box">
                {plant.adopted_by ? (
                  <div className="adopted-status">
                    Adopted by: <span className="roll-badge">{plant.adopted_by}</span>
                  </div>
                ) : (
                  <div className="adopt-form">
                    <input
                      type="text"
                      placeholder="Roll No (e.g. AU_101)"
                      value={rollNumbers[plant.id] || ""}
                      onChange={(e) => handleRollChange(plant.id, e.target.value)}
                      className="text-input"
                    />
                    <button
                      className="btn btn-primary"
                      onClick={() => handleAdoptClick(plant.id)}
                    >
                      Adopt
                    </button>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </section>
  );
}

export default Garden;

