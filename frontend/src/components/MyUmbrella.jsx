import { useState } from "react";
import { apiRequest } from "../services/api";

function MyUmbrella({ onReturned }) {
  const [rollNo, setRollNo] = useState("");
  const [borrow, setBorrow] = useState(null);
  const [stations, setStations] = useState([]);
  const [returnStation, setReturnStation] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState(false);

  async function checkBorrow(event) {
    event.preventDefault();

    setBorrow(null);
    setMessage("");
    setError(false);

    try {const data = await apiRequest(
        `/student/${encodeURIComponent(rollNo.trim())}/borrow`);

      setBorrow(data);

      const stationData = await apiRequest("/stations");
      setStations(stationData);
    } catch (err) {
      setError(true);
      setMessage(err.message);
    }
  }

  async function handleReturn() {
    if (!returnStation) {setError(true);setMessage("Please select a return station.");
      return;
    }

    setMessage("");
    setError(false);

    try {
      await apiRequest("/return", "POST", {roll_no: rollNo.trim(),station_id: returnStation});

      setMessage("Umbrella returned successfully!");
      setBorrow(null);
      setRollNo("");
      setReturnStation("");

      onReturned();
    } catch (err) {
      setError(true);
      setMessage(err.message);
    }
  }

  return (
    <section className="form-section" id="my-umbrella">
      <h2>My Umbrella</h2>

      <form onSubmit={checkBorrow}>
        <label>Student Roll Number</label>

        <input
          type="text"
          placeholder="Example: R1"
          value={rollNo}
          onChange={(event) => setRollNo(event.target.value)}
          required
        />

        <button type="submit">Check My Borrowing</button>
      </form>

      {borrow && (
        <div className="station-details">
          <h3>Active Borrowing</h3>

          <p>
            <strong>Roll Number:</strong>{" "}
            {borrow.roll_no || rollNo}
          </p>

          <p>
            <strong>Borrow ID:</strong>{" "}
            {borrow.id ?? borrow.borrow_id ?? "Recorded"}
          </p>

          <p>
            <strong>Borrowed From:</strong>{" "}
            {borrow.station_name ||
              borrow.from_station_name ||
              borrow.from_station_id ||
              "See borrowing record"}
          </p>

          <label>Return To</label>

          <select
            value={returnStation}
            onChange={(event) => setReturnStation(event.target.value)}
          >
            <option value="">Select a return station</option>

            {stations.map((station) => (
              <option
                key={station.id}
                value={station.id}
                disabled={station.free_slots <= 0}
              >
                {station.name} — {station.free_slots} free slots
              </option>
            ))}
          </select>

          <button type="button" onClick={handleReturn}>
            Return Umbrella
          </button>
        </div>
      )}

      {message && (
        <p className={error ? "error" : "success"}>
          {message}
        </p>
      )}
    </section>
  );
}

export default MyUmbrella;