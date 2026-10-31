import { useState, useEffect } from "react";
import Stations from "./components/Stations";
import MyUmbrella from "./components/MyUmbrella";

const API_URL = "http://127.0.0.1:8000";

export default function App() {
  const [stations, setStations] = useState([]);
  const [selectedStation, setSelectedStation] = useState(null);
  const [errorMessage, setErrorMessage] = useState("");
  const [isFiltered, setIsFiltered] = useState(false);

  const fetchStations = async () => {
    try {
      setErrorMessage("");
      const res = await fetch(`${API_URL}/stations`);
      const data = await res.json();
      setStations(data);
      setIsFiltered(false);
    } catch (err) {
      setErrorMessage("Could not connect to server.");
    }
  };

  const fetchNeedsAttention = async () => {
    try {
      setErrorMessage("");
      const res = await fetch(`${API_URL}/stations/attention`);
      const data = await res.json();
      setStations(data);
      setIsFiltered(true);
    } catch (err) {
      setErrorMessage("Could not connect to server.");
    }
  };

  useEffect(() => {
    fetchStations();
  }, []);

  const handleBorrow = async (stationId, rollNo) => {
    if (!rollNo?.trim()) {
      setErrorMessage("Roll number is required.");
      return;
    }
    setErrorMessage("");

    try {
      const res = await fetch(
        `${API_URL}/borrows?roll_no=${rollNo.trim()}&station_id=${stationId}`,
        { method: "POST" }
      );
      const data = await res.json();
      if (!res.ok) {
        setErrorMessage(data.detail || "Borrow failed.");
      } else {
        fetchStations();
      }
    } catch (err) {
      setErrorMessage("Error processing borrow request.");
    }
  };

  return (
    <div className="container">
      <h1>Campus Umbrella Sharing</h1>

      {errorMessage && <div className="alert-error">{errorMessage}</div>}

      <Stations
        stations={stations}
        onSelectStation={setSelectedStation}
        onNeedsAttention={fetchNeedsAttention}
        onResetFilter={fetchStations}
        onBorrow={handleBorrow}
        isFiltered={isFiltered}
      />

      {selectedStation && (
        <div className="modal-card">
          <h3>{selectedStation.name} Details</h3>
          <p><strong>Location:</strong> {selectedStation.location}</p>
          <p><strong>Capacity:</strong> {selectedStation.capacity}</p>
          <p><strong>Umbrellas Available:</strong> {selectedStation.umbrellas_available}</p>
          <p><strong>Free Slots:</strong> {selectedStation.capacity - selectedStation.umbrellas_available}</p>
          <button className="btn-secondary" onClick={() => setSelectedStation(null)}>Close</button>
        </div>
      )}

      <MyUmbrella
        stations={stations}
        apiUrl={API_URL}
        onError={setErrorMessage}
        onSuccess={fetchStations}
      />
    </div>
  );
}