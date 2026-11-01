

import { useState, useEffect } from "react";
import StationList from "./components/StationList";
import MyUmbrella from "./components/MyUmbrella";
import AddStation from "./components/AddStation";

const API_URL = "http://127.0.0.1:8001";

function App() {
  const [stations, setStations] = useState([]);
  const [rollNo, setRollNo] = useState("");
  const [message, setMessage] = useState("");

  useEffect(() => {
    getStations();
  }, []);

  function getStations() {
    fetch(`${API_URL}/stations`)
      .then(async (response) => {
        const data = await response.json();

        if (!response.ok) {
          setMessage(data.detail);
          return;
        }

        setStations(data);
      })
      .catch((error) => {
        setMessage("Unable to connect to the server");
        console.log("Fetch error:", error);
      });
  }

  function borrowUmbrella(stationId) {
    if (rollNo.trim() === "") {
      setMessage("Please enter your roll number");
      return;
    }

    fetch(`${API_URL}/borrow?roll_no=${rollNo}&station_id=${stationId}`, {
      method: "POST"
    })
      .then(async (response) => {
        const data = await response.json();

        if (!response.ok) {
          setMessage(data.detail);
          return;
        }

        setMessage("Umbrella borrowed successfully");
        getStations();
      })
      .catch((error) => {
        setMessage("Unable to connect to the server");
        console.log("Fetch error:", error);
      });
  }

  return (
    <>
      <h1>Umbrella Sharing Stations</h1>
      <input placeholder="Enter roll number" onChange={(e) => setRollNo(e.target.value)} />
      <p>{message}</p>
      <StationList stations={stations} onAdd={borrowUmbrella} />
      <MyUmbrella stations={stations} onAdd={getStations} />
      <AddStation onAdd={getStations} />
    </>
  );
}

export default App;
