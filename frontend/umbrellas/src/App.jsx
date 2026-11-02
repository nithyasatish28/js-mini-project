import { useState, useEffect } from "react";
import StationList from "./components/StationList";
import MyUmbrella from "./components/MyUmbrella";
import AddStation from "./components/AddStation";
const API_URL = "http://127.0.0.1:8001";
function App() {
  const [stations, setStations] = useState([]);
  const [message, setMessage] = useState("");
  function loadStations() {
    fetch(API_URL + "/stations")
      .then((response) => response.json())
      .then((data) => setStations(data));
  }
  useEffect(() => {
    loadStations();
  }, []);
  // if the API sent an error show it, otherwise show the success text and reload
  function handleResult(data, successMessage ) {
    if (typeof data.detail === "string") {
      setMessage(data.detail);
    } else if (data.detail) {
      setMessage("Please fill all fields correctly");
    } else {
      setMessage(successMessage);
      loadStations();
    }
  }
  return (
    <>
      <h1>Umbrella Sharing</h1>
      <p>{message}</p>
      <StationList API_URL={API_URL} stations={stations} handleResult={handleResult} />
      <MyUmbrella API_URL={API_URL} stations={stations} handleResult={handleResult} setMessage={setMessage} />
      <AddStation API_URL={API_URL} handleResult={handleResult} />
    </>
  );
}
export default App;import { useState, useEffect } from "react";
import StationList from "./components/StationList";
import MyUmbrella from "./components/MyUmbrella";
import AddStation from "./components/AddStation";
const API_URL = "http://127.0.0.1:8001";
function App() {
  const [stations, setStations] = useState([]);
  const [message, setMessage] = useState("");
  function loadStations() {
    fetch(API_URL + "/stations")
      .then((response) => response.json())
      .then((data) => setStations(data));
  }
  useEffect(() => {
    loadStations();
  }, []);
  // if the API sent an error show it, otherwise show the success text and reload
  function handleResult(data, successMessage ) {
    if (typeof data.detail === "string") {
      setMessage(data.detail);
    } else if (data.detail) {
      setMessage("Please fill all fields correctly");
    } else {
      setMessage(successMessage);
      loadStations();
    }
  }
  return (
    <>
      <h1>Umbrella Sharing</h1>
      <p>{message}</p>
      <StationList API_URL={API_URL} stations={stations} handleResult={handleResult} />
      <MyUmbrella API_URL={API_URL} stations={stations} handleResult={handleResult} setMessage={setMessage} />
      <AddStation API_URL={API_URL} handleResult={handleResult} />
    </>
  );
}
export default App;
