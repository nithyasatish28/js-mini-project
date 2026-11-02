import { useState } from "react";

function AddPlant({ onAddPlant }) {
  const [name, setName] = useState("");
  const [type, setType] = useState("succulent");
  const [location, setLocation] = useState("");
  const [waterEveryDays, setWaterEveryDays] = useState(3);
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    if (!name.trim() || !location.trim()) {
      return;
    }

    setIsSubmitting(true);
    const success = await onAddPlant({
      name: name.trim(),
      type: type.trim().toLowerCase(),
      location: location.trim(),
      water_every_days: parseInt(waterEveryDays, 10),
    });

    if (success) {
     
      setName("");
      setType("succulent");
      setLocation("");
      setWaterEveryDays(3);
    }
    setIsSubmitting(false);
  }

  return (
    <section className="section add-plant-section">
      <div className="section-header">
        <h2>➕ Add a Plant</h2>
        <p>Garden team: Register a new campus plant for students to adopt.</p>
      </div>

      <form onSubmit={handleSubmit} className="add-plant-form">
        <div className="form-grid">
          <div className="form-group">
            <label htmlFor="plant-name"><strong>Plant Name</strong></label>
            <input
              id="plant-name"
              type="text"
              placeholder="e.g. Snake Plant"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
              className="text-input"
            />
          </div>

          <div className="form-group">
            <label htmlFor="plant-type"><strong>Plant Type</strong></label>
            <select
              id="plant-type"
              value={type}
              onChange={(e) => setType(e.target.value)}
              className="select-input"
            >
              <option value="succulent">succulent</option>
              <option value="flowering">flowering</option>
              <option value="herb">herb</option>
              <option value="indoor">indoor</option>
              <option value="tree">tree</option>
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="plant-location"><strong>Location on Campus</strong></label>
            <input
              id="plant-location"
              type="text"
              placeholder="e.g. Science Block Balcony"
              value={location}
              onChange={(e) => setLocation(e.target.value)}
              required
              className="text-input"
            />
          </div>

          <div className="form-group">
            <label htmlFor="plant-water-days">
              <strong>Water Every (Days, 1-14)</strong>
            </label>
            <input
              id="plant-water-days"
              type="number"
              min="1"
              max="14"
              value={waterEveryDays}
              onChange={(e) => setWaterEveryDays(e.target.value)}
              required
              className="text-input"
            />
          </div>
        </div>

        <button
          type="submit"
          className="btn btn-primary submit-btn"
          disabled={isSubmitting}
        >
          {isSubmitting ? "Adding Plant..." : "Add Plant to Garden"}
        </button>
      </form>
    </section>
  );
}

export default AddPlant;

