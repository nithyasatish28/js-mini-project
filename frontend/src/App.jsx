import { useState, useEffect } from "react";
import Stations from "./components/Stations";
import MyUmbrella from "./components/MyUmbrella";
import AddStation from "./components/AddStation";
import "./App.css";

const API_URL = "http://localhost:8001";

export default function App() {
  const [stations, setStations] = useState([]);
  const [attentionStations, setAttentionStations] = useState([]);
  const [rollNo, setRollNo] = useState("");
  const [activeTab, setActiveTab] = useState("all");
  const [selected, setSelected] = useState(null);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  const [loading, setLoading] = useState(true);

  async function fetchStations() {
    try {
      const [stationsRes, attentionRes] = await Promise.all([
        fetch(`${API_URL}/stations`),
        fetch(`${API_URL}/stations/needs-attention`)
      ]);

      const stationsData = await stationsRes.json();
      const attentionData = await attentionRes.json();

      if (!stationsRes.ok) throw new Error(stationsData.detail);
      if (!attentionRes.ok) throw new Error(attentionData.detail);

      setStations(stationsData);
      setAttentionStations(attentionData);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    fetchStations();
  }, []);

  async function handleBorrow(stationId) {
    if (!rollNo.trim()) {
      setError("Please enter your student roll number.");
      return;
    }

    setError("");
    setNotice("");

    try {
      const res = await fetch(
        `${API_URL}/stations/${stationId}/borrow?roll_no=${encodeURIComponent(rollNo.trim())}`,
        { method: "POST" }
      );

      const data = await res.json();
      if (!res.ok) throw new Error(data.detail);

      setNotice("Umbrella borrowed successfully.");
      await fetchStations();
    } catch (err) {
      setError(err.message);
    }
  }

  async function handleStationSelect(id) {
    setError("");

    try {
      const res = await fetch(`${API_URL}/stations/${id}`);
      const data = await res.json();

      if (!res.ok) throw new Error(data.detail);

      setSelected(data);
    } catch (err) {
      setError(err.message);
    }
  }

  function changeTab(tab) {
    setActiveTab(tab);
    setError("");
    setNotice("");
    setSelected(null);
  }

  const tabs = [
    { id: "all", label: "All Stations", icon: "▦" },
    { id: "attention", label: "Needs Attention", icon: "⚡" },
    { id: "borrow", label: "My Borrow", icon: "☂" },
    { id: "add", label: "Add New Station", icon: "＋" }
  ];

  const visibleStations = activeTab === "attention"
    ? attentionStations
    : stations;

  const totalUmbrellas = stations.reduce(
    (total, station) => total + station.umbrellas_available, 0
  );

  return (
    <div className="app-shell">
      <header className="topbar">
        <div className="brand">
          <div className="brand-icon">☂</div>
          <div>
            <h2>Umbra</h2>
            <span>CAMPUS MOBILITY</span>
          </div>
        </div>
        <div className="topbar-right">
          <span className="live-indicator">SERVICE ACTIVE</span>
          <span className="portal-label">STUDENT PORTAL</span>
        </div>
      </header>

      <main className="dashboard">
        <section className="page-heading">
          <span className="eyebrow">SMART CAMPUS NETWORK</span>
          <h1>Umbrella Sharing System</h1>
          <p>Manage stations, borrow umbrellas and return them anywhere on campus.</p>
        </section>

        <nav className="tab-navigation">
          {tabs.map(tab => (
            <button
              key={tab.id}
              className={`tab-button ${activeTab === tab.id ? "active" : ""}`}
              onClick={() => changeTab(tab.id)}
            >
              <span>{tab.icon}</span>
              {tab.label}
            </button>
          ))}
        </nav>

        {(activeTab === "all" || activeTab === "attention" || activeTab === "borrow") && (
          <div className="student-entry">
            <label htmlFor="rollNo">STUDENT ROLL NUMBER</label>
            <input
              id="rollNo"
              type="text"
              placeholder="Enter your roll number"
              value={rollNo}
              onChange={e => setRollNo(e.target.value)}
            />
          </div>
        )}

        {error && (
          <div className="error-message">
            <span>{error}</span>
            <button onClick={() => setError("")}>✕</button>
          </div>
        )}

        {notice && (
          <div className="success-message">
            {notice}
          </div>
        )}

        {loading && (
          <div className="loading-message">
            Loading campus stations...
          </div>
        )}

        {!loading && (activeTab === "all" || activeTab === "attention") && (
          <Stations
            stations={visibleStations}
            onSelectStation={handleStationSelect}
            onBorrow={handleBorrow}
          />
        )}

        {!loading && activeTab === "borrow" && (
          <div className="tab-content">
            <MyUmbrella
              stations={stations}
              rollNo={rollNo}
              apiUrl={API_URL}
              onError={setError}
              onSuccess={fetchStations}
            />
          </div>
        )}

        {!loading && activeTab === "add" && (
          <div className="tab-content">
            <AddStation
              apiUrl={API_URL}
              onError={setError}
              onStationAdded={fetchStations}
            />
          </div>
        )}

        {selected && (activeTab === "all" || activeTab === "attention") && (
          <section className="detail-panel">
            <div>
              <span className="eyebrow">STATION INFORMATION</span>
              <h2>{selected.name}</h2>
              <p>{selected.location}</p>
            </div>
            <div className="detail-numbers">
              <span>Capacity: <strong>{selected.capacity}</strong></span>
              <span>Available: <strong>{selected.umbrellas_available}</strong></span>
              <span>Free slots: <strong>{selected.free_slots}</strong></span>
            </div>
            <button
              className="secondary-button"
              onClick={() => setSelected(null)}
            >
              Close
            </button>
          </section>
        )}

        <footer className="footer">
          <span>UMBRA — CAMPUS UMBRELLA SHARING</span>
          <span>BUILT FOR SMARTER CAMPUS MOBILITY</span>
        </footer>
      </main>
    </div>
  );
}