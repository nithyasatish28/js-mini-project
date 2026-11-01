import React, { useState } from "react";
import StationList from "./components/StationList.jsx";
import MyUmbrella from "./components/MyUmbrella.jsx";
import AddStation from "./components/AddStation.jsx";
import BorrowUmbrella from "./components/BorrowUmbrella.jsx";
import ActiveBorrows from "./components/ActiveBorrows.jsx";
import "./styles/app.css";

const API_URL = "http://127.0.0.1:8001";

function App() {
  // Changing this number tells the components to fetch the data again
  const [refreshKey, setRefreshKey] = useState(0);

  function refreshStations() {
    setRefreshKey((count) => count + 1);
  }

  return (
    <div className="app">
      <header className="header">
        <h1>Campus Umbrella Sharing</h1>
        <p>Borrow anywhere. Return anywhere.</p>
      </header>

      <main>
        <StationList apiUrl={API_URL} refreshKey={refreshKey} />

        <ActiveBorrows apiUrl={API_URL} refreshKey={refreshKey} />

        <div className="sections">
          <BorrowUmbrella
            apiUrl={API_URL}
            refreshKey={refreshKey}
            onBorrowed={refreshStations}
          />
          <MyUmbrella apiUrl={API_URL} onReturned={refreshStations} />
          <AddStation apiUrl={API_URL} onStationAdded={refreshStations} />
        </div>
      </main>
    </div>
  );
}

export default App;