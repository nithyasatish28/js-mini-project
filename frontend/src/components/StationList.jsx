import React from "react";
import { useState, useEffect } from "react";
import StationCard from "./StationCard";

function StationList({ apiUrl, refreshKey }) {
  const [stations, setStations] = useState([]);

  // Fetch stations from backend
  async function getStations() {
    const response = await fetch(`${apiUrl}/stations`);
    const data = await response.json();

    setStations(data);
  }

  // Run when component loads, and again whenever refreshKey changes
  useEffect(() => {
    getStations();
  }, [refreshKey]);

  // Select a station
  function handleSelect(stationId) {
    console.log("Selected station:", stationId);
  }

  return (
    <section className="station-section">
      <h2>Umbrella Stations</h2>

      <div className="station-list">
        {stations.length === 0 ? (
          <p>Loading stations...</p>
        ) : (
          stations.map((station) => (
            <StationCard
              key={station.id}
              station={station}
              onSelect={handleSelect}
            />
          ))
        )}
      </div>
    </section>
  );
}

export default StationList;