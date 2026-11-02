import { useState } from "react";
import StationList from "./components/StationList";
import AddStation from "./components/AddStation";
import MyUmbrella from "./components/MyUmbrella";
import "./index.css";

function App() {
  const [refresh, setRefresh] = useState(0);

  function updateStations() {
    setRefresh(refresh + 1);
  }

  return (
    <div>
      <h1>Umbrella Sharing System</h1>

      <StationList refresh={refresh} />

      <AddStation refresh={updateStations} />

      <MyUmbrella refresh={updateStations} />
    </div>
  );
}

export default App;