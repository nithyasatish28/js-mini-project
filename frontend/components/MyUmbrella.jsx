import { useState } from "react";

function MyUmbrella({ apiUrl }) {
  const [rollNo, setRollNo] = useState("");
  const [borrow, setBorrow] = useState(null);
  const [stations, setStations] = useState([]);
  const [returnStation, setReturnStation] = useState("");

  const [message, setMessage] = useState("");

  // Check whether the student has borrowed an umbrella
  async function checkBorrow() {
    setMessage("");
    setBorrow(null);

    try {
      const response = await fetch(`${apiUrl}/borrow/${rollNo}`);
      const data = await response.json();

      if (response.ok) {
        setBorrow(data);

        // Get all stations
        const stationResponse = await fetch(`${apiUrl}/stations`);
        const stationData = await stationResponse.json();

        setStations(stationData);
      } else {
        setMessage(data.detail);
      }
    } catch (error) {
      setMessage("Unable to connect to the server.");
    }
  }

  // Return the umbrella
  async function handleReturn() {
    if (returnStation === "") {
      setMessage("Please select a return station.");
      return;
    }

    try {
      const response = await fetch(
        `${apiUrl}/return/${borrow.borrow_id}`,
        {
          method: "PATCH",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            to_station_id: Number(returnStation)
          })
        }
      );

      const data = await response.json();

      if (response.ok) {
        setMessage("Umbrella returned successfully!");
        setBorrow(null);
        setRollNo("");
        setReturnStation("");
      } else {
        setMessage(data.detail);
      }
    } catch (error) {
      setMessage("Unable to connect to the server.");
    }
  }

  return (
    <section className="my-umbrella">
      <h2>My Umbrella</h2>

      <input
        type="text"
        placeholder="Enter roll number (Example: R1)"
        value={rollNo}
        onChange={(e) => setRollNo(e.target.value)}
      />

      <button onClick={checkBorrow}>
        Check My Borrow
      </button>

      {borrow && (
        <div>
          <h3>Active Borrow</h3>

          <p>Roll Number: {borrow.roll_no}</p>
          <p>Borrowed From: {borrow.station_name}</p>
          <p>Borrow ID: {borrow.borrow_id}</p>

          <label>Return Station:</label>

          <select
            value={returnStation}
            onChange={(e) => setReturnStation(e.target.value)}
          >
            <option value="">Select a station</option>

            {stations.map((station) => (
              <option key={station.id} value={station.id}>
                {station.name}
              </option>
            ))}
          </select>

          <button onClick={handleReturn}>
            Return Umbrella
          </button>
        </div>
      )}

      {message && <p className="error">{message}</p>}
    </section>
  );
}

export default MyUmbrella;