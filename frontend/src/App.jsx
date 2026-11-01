import { useState, useEffect } from "react";
import EquipmentCard from "./components/EquipmentCard";
import MyBookings from "./components/MyBookings";
import AddEquipment from "./components/AddEquipment";
import "./index.css";

const API_URL = "http://127.0.0.1:8001";

const TYPES = ["", "microscope", "oscilloscope", "3d-printer", "laptop", "camera"];

function App() {
  const [equipment, setEquipment] = useState([]);
  const [typeFilter, setTypeFilter] = useState("");

  function loadEquipment(filter) {
    const url = filter
      ? `${API_URL}/equipments?type=${filter}`
      : `${API_URL}/equipments`;
    fetch(url)
      .then((res) => res.json())
      .then((data) => setEquipment(data));
  }

  useEffect(() => {
    loadEquipment(typeFilter);
  }, [typeFilter]);

  return (
    <>
      <div className="app-header">
        <h1>🔬 Lab Equipment Booking</h1>
      </div>

      <div className="section">
        <h2>Equipment</h2>
        <div className="filter-row">
          <label>Filter by type:</label>
          <select value={typeFilter} onChange={(e) => setTypeFilter(e.target.value)}>
            {TYPES.map((t) => (
              <option key={t} value={t}>{t === "" ? "All" : t}</option>
            ))}
          </select>
        </div>
        <ul className="equipment-list">
          {equipment.map((item) => (
            <EquipmentCard
              key={item.id}
              item={item}
              apiUrl={API_URL}
              onRefresh={() => loadEquipment(typeFilter)}
            />
          ))}
        </ul>
      </div>

      <div className="section">
        <MyBookings apiUrl={API_URL} />
      </div>

      <div className="section">
        <AddEquipment apiUrl={API_URL} onRefresh={() => loadEquipment(typeFilter)} />
      </div>
    </>
  );
}

export default App;
