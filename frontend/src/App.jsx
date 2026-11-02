import { useState, useEffect } from "react";
import Garden from "./Components/Garden";
import MyPlants from "./Components/MyPlants";
import AddPlant from "./Components/AddPlant";


const API_URL = "http://127.0.0.1:8001";

function App() {
  const [plants, setPlants] = useState([]);
  const [loading, setLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState("");
  const [successMessage, setSuccessMessage] = useState("");
  const [selectedType, setSelectedType] = useState("");
  const [onlyNeedsWater, setOnlyNeedsWater] = useState(false);
  const [activeTab, setActiveTab] = useState("all"); // 'all', 'garden', 'my-plants', 'add-plant'

  async function loadPlants(typeFilter = selectedType, needsWaterOnly = onlyNeedsWater) {
    setLoading(true);
    try {
      let url = `${API_URL}/plants`;
      if (needsWaterOnly) {
        url = `${API_URL}/plants/needs-water`;
      } else if (typeFilter) {
        url = `${API_URL}/plants?type=${encodeURIComponent(typeFilter)}`;
      }

      const response = await fetch(url);
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Failed to fetch plants");
      }
      const data = await response.json();
      setPlants(data);
    } catch (err) {
      setErrorMessage(err.message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadPlants();
  }, []);

 
  function handleTypeChange(newType) {
    setSelectedType(newType);
    setOnlyNeedsWater(false);
    loadPlants(newType, false);
  }


  function handleToggleNeedsWater() {
    const nextVal = !onlyNeedsWater;
    setOnlyNeedsWater(nextVal);
    if (nextVal) {
      setSelectedType("");
    }
    loadPlants(nextVal ? "" : selectedType, nextVal);
  }

  
  async function handleAdopt(plantId, rollNo) {
    setErrorMessage("");
    setSuccessMessage("");

    if (!rollNo || !rollNo.trim()) {
      setErrorMessage("Please enter a roll number to adopt a plant.");
      return;
    }

    try {
      const response = await fetch(`${API_URL}/plants/${plantId}/adopt`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ roll_no: rollNo.trim() }),
      });

      const data = await response.json();
      if (!response.ok) {
       
        throw new Error(data.detail || "Failed to adopt plant");
      }

      setSuccessMessage(`Successfully adopted "${data.name}" as ${data.adopted_by}!`);
     
      await loadPlants();
    } catch (err) {
      setErrorMessage(err.message);
    }
  }


  async function handleWater(plantId, rollNo) {
    setErrorMessage("");
    setSuccessMessage("");

    if (!rollNo || !rollNo.trim()) {
      setErrorMessage("Roll number is required to water a plant.");
      return;
    }

    try {
      const response = await fetch(`${API_URL}/plants/${plantId}/water`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ roll_no: rollNo.trim() }),
      });

      const data = await response.json();
      if (!response.ok) {
      
        throw new Error(data.detail || "Failed to water plant");
      }

      setSuccessMessage("💧 Plant watered successfully!");
      
      await loadPlants();
    } catch (err) {
      setErrorMessage(err.message);
    }
  }

 
  async function handleGiveUp(plantId) {
    setErrorMessage("");
    setSuccessMessage("");

    try {
      const response = await fetch(`${API_URL}/plants/${plantId}/unadopt`, {
        method: "PATCH",
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.detail || "Failed to give up plant");
      }

      setSuccessMessage(`Gave up "${data.name}". It is now available for adoption.`);
      
      await loadPlants();
    } catch (err) {
      setErrorMessage(err.message);
    }
  }

  async function handleAddPlant(newPlant) {
    setErrorMessage("");
    setSuccessMessage("");

    try {
      const response = await fetch(`${API_URL}/plants`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(newPlant),
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.detail || "Failed to add plant");
      }

      setSuccessMessage(`Added "${data.name}" to the campus garden!`);
      
      await loadPlants();
      return true;
    } catch (err) {
      setErrorMessage(err.message);
      return false;
    }
  }

  return (
    <div className="app-container">
      {/* Header */}
      <header className="app-header">
        <div className="header-content">
          <h1>🌱 Adopt-a-Plant</h1>
          <p className="subtitle">
            Adopt campus plants, keep them watered, and track green life around campus.
          </p>
        </div>

        {/* View Switcher Navigation */}
        <nav className="tab-nav">
          <button
            className={`tab-btn ${activeTab === "all" ? "active" : ""}`}
            onClick={() => setActiveTab("all")}
          >
            All Sections
          </button>
          <button
            className={`tab-btn ${activeTab === "garden" ? "active" : ""}`}
            onClick={() => setActiveTab("garden")}
          >
            Garden
          </button>
          <button
            className={`tab-btn ${activeTab === "my-plants" ? "active" : ""}`}
            onClick={() => setActiveTab("my-plants")}
          >
            My Plants
          </button>
          <button
            className={`tab-btn ${activeTab === "add-plant" ? "active" : ""}`}
            onClick={() => setActiveTab("add-plant")}
          >
            Add a Plant
          </button>
        </nav>
      </header>

      {/* Global Notifications */}
      {errorMessage && (
        <div className="alert alert-error">
          <span>⚠️ {errorMessage}</span>
          <button className="close-btn" onClick={() => setErrorMessage("")}>
            ✕
          </button>
        </div>
      )}

      {successMessage && (
        <div className="alert alert-success">
          <span>✅ {successMessage}</span>
          <button className="close-btn" onClick={() => setSuccessMessage("")}>
            ✕
          </button>
        </div>
      )}

      {loading && <p className="loading-banner">Loading plant data...</p>}

      {/* Main Content with 3 Parts */}
      <main className="main-content">
        {(activeTab === "all" || activeTab === "garden") && (
          <Garden
            plants={plants}
            selectedType={selectedType}
            onTypeChange={handleTypeChange}
            onlyNeedsWater={onlyNeedsWater}
            onToggleNeedsWater={handleToggleNeedsWater}
            onAdopt={handleAdopt}
          />
        )}

        {(activeTab === "all" || activeTab === "my-plants") && (
          <MyPlants
            plants={plants}
            onWater={handleWater}
            onGiveUp={handleGiveUp}
            apiUrl={API_URL}
          />
        )}

        {(activeTab === "all" || activeTab === "add-plant") && (
          <AddPlant onAddPlant={handleAddPlant} />
        )}
      </main>

      <footer className="app-footer">
        <p>Adopt-a-Plant · FastAPI + SQLite Backend on Port 8001 · React Frontend</p>
      </footer>
    </div>
  );
}

export default App;
