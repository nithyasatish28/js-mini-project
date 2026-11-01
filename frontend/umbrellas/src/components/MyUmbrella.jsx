
import { useState } from "react";

const API_URL = "http://127.0.0.1:8001";

function MyUmbrella({ stations, onAdd }) {
  const [rollNo, setRollNo] = useState("");
  const [borrow, setBorrow] = useState(null);
  const [stationId, setStationId] = useState("");
  const [message, setMessage] = useState("");

  function getUmbrella() {
    fetch(`${API_URL}/students/${rollNo}/umbrella`)
      .then(async (response) => {
        const data = await response.json();

        if (!response.ok) {
          setMessage(data.detail);
          setBorrow(null);
          return;
        }

        setBorrow(data);
        setMessage("");
      })
      .catch((error) => console.log("Fetch error:", error));
  }

  function returnUmbrella() {
    fetch(`${API_URL}/borrows/${borrow.borrow_id}/return?station_id=${stationId}`, {
      method: "PATCH"
    })
      .then(async (response) => {
        const data = await response.json();

        if (!response.ok) {
          setMessage(data.detail);
          return;
        }

        setBorrow(null);
        setMessage("Umbrella returned successfully");
        onAdd();
      })
      .catch((error) => console.log("Fetch error:", error));
  }

  return (
    <>
      <h2>My Umbrella</h2>
      <input placeholder="Roll number" onChange={(e) => setRollNo(e.target.value)} />
      <button onClick={getUmbrella}>Show</button>
      <p>{message}</p>

      {borrow && (
        <>
          <p>{borrow.station_name}</p>
          <select onChange={(e) => setStationId(e.target.value)}>
            {stations.map((station) => (
              <option key={station.id} value={station.id}>{station.name}</option>
            ))}
          </select>
          <button onClick={returnUmbrella}>Return</button>
        </>
      )}
    </>
  );
}

export default MyUmbrella;