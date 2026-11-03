import { useEffect, useState } from "react";
import { apiRequest } from "../services/api";

function BorrowUmbrella({ refreshKey, onBorrowed }) {
  const [stations, setStations] = useState([]);
  const [rollNo, setRollNo] = useState("");
  const [stationId, setStationId] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState(false);

  useEffect(() => {
    async function loadStations() {
      try {
        const data = await apiRequest("/stations");
        setStations(data);
      } catch (err) {
        setError(true);
        setMessage(err.message);
      }
    }

    loadStations();
  }, [refreshKey]);

  async function handleBorrow(event) {
    event.preventDefault();

    setMessage("");
    setError(false);

    try {
      const data = await apiRequest("/borrow", "POST", {
        roll_no: rollNo.trim(),
        station_id: stationId
      });

      setMessage(
        typeof data === "string"
          ? data
          : "Umbrella borrowed successfully!"
      );

      setRollNo("");
      setStationId("");

      onBorrowed();
    } catch (err) {
      setError(true);
      setMessage(err.message);
    }
  }

  return (
    <section className="form-section" id="borrow">
      <h2>Borrow an Umbrella</h2>

      <form onSubmit={handleBorrow}>
        <label>Student Roll Number</label>

        <input
          type="text"
          placeholder="Example: R1"
          value={rollNo}
          onChange={(event) => setRollNo(event.target.value)}
          required
        />

        <label>Choose Station</label>

        <select
          value={stationId}
          onChange={(event) => setStationId(event.target.value)}
          required
        >
          <option value="">Select a station</option>

          {stations.map((station) => (
            <option
              key={station.id}
              value={station.id}
              disabled={station.umbrellas_available === 0}
            >
              {station.name} — {station.umbrellas_available} available
            </option>
          ))}
        </select>

        <button type="submit">Borrow Umbrella</button>
      </form>

      {message && (
        <p className={error ? "error" : "success"}>
          {message}
        </p>
      )}
    </section>
  );
}

export default BorrowUmbrella;