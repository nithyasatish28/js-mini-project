import React from "react";
import StationList from "./components/StationList.jsx";
import MyUmbrella from "./components/MyUmbrella.jsx";
import AddStation from "./components/AddStation.jsx";
import "./styles/app.css";

const API_URL = "http://127.0.0.1:8001";

function App() {
  return (
    <div className="app">
      <header className="header">
        <h1>Campus Umbrella Sharing</h1>
        <p>Borrow anywhere. Return anywhere.</p>
      </header>

      <main>
        <StationList apiUrl={API_URL} />

        <div className="sections">
          <MyUmbrella apiUrl={API_URL} />
          <AddStation apiUrl={API_URL} />
        </div>
      </main>
    </div>
  );
}

export default App;
