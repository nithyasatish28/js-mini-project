import React from "react";
import { useState, useEffect } from "react";

function BorrowUmbrella({ apiUrl, refreshKey, onBorrowed }) {
  const [stations, setStations] = useState([]);
  const [rollNo, setRollNo] = useState("");
  const [stationId, setStationId] = useState("");

  // Load the stations so the student can pick one
  useEffect(() => {
    async function loadStations() {
      try {
        const response = await fetch(`${apiUrl}/stations`);
        const data = await response.json();
        setStations(data);
      } catch (error) {
        alert("Unable to connect to the server.");
      }
    }

    loadStations();
  }, [apiUrl, refreshKey]);

  async function borrowUmbrella(event) {
    event.preventDefault();

    if (stationId === "") {
      alert("Please select a station.");
      return;
    }

    try {
      const response = await fetch(`${apiUrl}/borrow`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          roll_no: rollNo.trim().toUpperCase(),
          from_station_id: Number(stationId)
        })
      });

      const data = await response.json();

      if (!response.ok) {
        // Validation errors come back as a list, so show a simple message for those
        alert(
          typeof data.detail === "string"
            ? data.detail
            : "Please check your roll number (Example: R1)."
        );
        return;
      }

      alert("Umbrella borrowed successfully!");

      setRollNo("");
      setStationId("");
      onBorrowed();

    } catch (error) {
      alert("Unable to connect to the server.");
    }
  }

  return (
    <form onSubmit={borrowUmbrella}>
      <h2>Borrow an Umbrella</h2>

      <input
        type="text"
        placeholder="Your roll number (Example: R1)"
        pattern="[Rr][1-9][0-9]*"
        title="Roll number like R1 or R23"
        value={rollNo}
        onChange={(e) => setRollNo(e.target.value)}
        required
      />

      <select
        value={stationId}
        onChange={(e) => setStationId(e.target.value)}
        required
      >
        <option value="">Pick a station</option>

        {stations.map((station) => (
          <option
            key={station.id}
            value={station.id}
            disabled={station.umbrellas_available === 0}
          >
            {station.name} ({station.umbrellas_available} left)
          </option>
        ))}
      </select>

      <button type="submit">Take Umbrella</button>
    </form>
  );
}

export default BorrowUmbrella;