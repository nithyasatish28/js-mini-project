
import { useState, useEffect } from "react";
import StationList from "./components/StationList";
import MyUmbrella from "./components/MyUmbrella";
import AddStation from "./components/AddStation";

const API_URL = "http://127.0.0.1:8001";

function App() {
  const [stations, setStations] = useState([]);
  const [message, setMessage] = useState("");

  useEffect(() => {
    fetch(`${API_URL}/stations`)
      .then((response) => response.json())
      .then((data) => setStations(data));
  }, []);

function getStations() {
  fetch(`${API_URL}/stations`)
    .then(async (response) => {
      const data = await response.json();

      if (!response.ok) {
        console.log("API error:", data);
        return;
      }

      setStations(data);
    })
    .catch((error) => console.log("Fetch error:", error));
}

  return (
    <>
      <h1>Umbrella Sharing Stations</h1>
      <p>{message}</p>
      <StationList stations={stations} onAdd={getStations} />
      <MyUmbrella stations={stations} onAdd={getStations} />
      <AddStation onAdd={getStations} />
    </>
  );
}

export default App;
