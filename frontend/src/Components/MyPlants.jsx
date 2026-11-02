import { useState } from "react";

function MyPlants({
  plants,
  onWater,
  onGiveUp,
  apiUrl,
}) {
  const [rollInput, setRollInput] = useState("");
  const [activeRoll, setActiveRoll] = useState("");
  const [expandedPlantId, setExpandedPlantId] = useState(null);
  const [plantWaterings, setPlantWaterings] = useState({});
  const [loadingWaterings, setLoadingWaterings] = useState(false);
  const [wateringsError, setWateringsError] = useState("");

  function handleShow() {
    if (rollInput.trim()) {
      setActiveRoll(rollInput.trim());
      setExpandedPlantId(null);
    }
  }


  const myAdoptedPlants = activeRoll
    ? plants.filter(
        (plant) =>
          plant.adopted_by &&
          plant.adopted_by.toLowerCase() === activeRoll.toLowerCase()
      )
    : [];


  async function toggleWaterings(plantId) {
    if (expandedPlantId === plantId) {
      setExpandedPlantId(null);
      return;
    }

    setLoadingWaterings(true);
    setWateringsError("");

    try {
      const response = await fetch(`${apiUrl}/plants/${plantId}`);
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Could not fetch waterings");
      }
      const data = await response.json();
      setPlantWaterings((prev) => ({
        ...prev,
        [plantId]: data.waterings || [],
      }));
      setExpandedPlantId(plantId);
    } catch (err) {
      setWateringsError(err.message);
    } finally {
      setLoadingWaterings(false);
    }
  }

  return (
    <section className="section my-plants-section">
      <div className="section-header">
        <h2>🌱 My Adopted Plants</h2>
        <p>Enter your roll number to manage your plants, water them, or view watering history.</p>
      </div>

      {/* Roll Number Lookup Form */}
      <div className="toolbar roll-lookup-bar">
        <label htmlFor="roll-search"><strong>Student Roll Number:</strong></label>
        <div className="search-group">
          <input
            id="roll-search"
            type="text"
            placeholder="e.g. AU_101"
            value={rollInput}
            onChange={(e) => setRollInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleShow()}
            className="text-input"
          />
          <button className="btn btn-primary" onClick={handleShow}>
            Show
          </button>
        </div>
      </div>

      {wateringsError && <div className="alert alert-error">{wateringsError}</div>}

      {/* Content based on whether roll number has been entered */}
      {!activeRoll ? (
        <p className="empty-message">Type your roll number and click <strong>Show</strong> to view your plants.</p>
      ) : myAdoptedPlants.length === 0 ? (
        <p className="empty-message">No plants adopted yet for roll number <strong>{activeRoll}</strong>.</p>
      ) : (
        <div className="plant-grid">
          {myAdoptedPlants.map((plant) => (
            <div key={plant.id} className="plant-card my-plant-card">
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

              {/* Action Buttons: Water and Give up */}
              <div className="card-actions">
                <button
                  className="btn btn-water"
                  onClick={() => onWater(plant.id, activeRoll)}
                >
                  💧 Water
                </button>
                <button
                  className="btn btn-danger"
                  onClick={() => onGiveUp(plant.id)}
                >
                  Give up
                </button>
                <button
                  className="btn btn-secondary"
                  onClick={() => toggleWaterings(plant.id)}
                >
                  {expandedPlantId === plant.id ? "Hide History" : "📜 History"}
                </button>
              </div>

              {/* Waterings History (E2) */}
              {expandedPlantId === plant.id && (
                <div className="waterings-history">
                  <h4>Watering History (Newest first)</h4>
                  {loadingWaterings ? (
                    <p className="loading-text">Loading waterings...</p>
                  ) : !plantWaterings[plant.id] || plantWaterings[plant.id].length === 0 ? (
                    <p className="empty-history">No waterings logged yet.</p>
                  ) : (
                    <ul className="waterings-list">
                      {plantWaterings[plant.id].map((w) => (
                        <li key={w.id} className="watering-item">
                          <span>📅 {w.watered_on}</span>
                          <span className="watered-by">by {w.roll_no}</span>
                        </li>
                      ))}
                    </ul>
                  )}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </section>
  );
}

export default MyPlants;

