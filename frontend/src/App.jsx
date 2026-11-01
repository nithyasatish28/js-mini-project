import { useState } from "react";
import RaiseComplaint from "./components/RaiseComplaint";
import Complaints from "./components/Complaints";
import Warden from "./components/Warden";

const API_URL = "http://127.0.0.1:8001";



function App() {
  const [refresh, setRefresh] = useState(0);

  function handleAction() {
    setRefresh((prev) => prev + 1);
  }

  return (
    <div className="container">
      <header>
        <h1>Hostel Complaint Tracker</h1>
      </header>

      <main className="layout">
        <div className="column">
          <RaiseComplaint API_URL={API_URL} onAction={handleAction} />
          <Complaints API_URL={API_URL} refresh={refresh} onAction={handleAction} />
        </div>
        <div className="column">
          <Warden API_URL={API_URL} refresh={refresh} onAction={handleAction} />
        </div>
      </main>
    </div>
  );
}

export default App;
