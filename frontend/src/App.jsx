import { useState } from "react";

import WardenDashboard from "./components/WardenDashboard";
import MyComplaints from "./components/MyComplaints";
import RaiseComplaint from "./components/RaiseComplaint";

function App() {
  const [refreshKey, setRefreshKey] = useState(0);

  function refreshPage() {
    setRefreshKey(refreshKey + 1);
  }

  return (
    <div className="app-container">
      <header className="page-header">
        <h1>Hostel Complaint Tracker</h1>
        <p>Manage and track hostel complaints easily.</p>
      </header>

      <section className="dashboard-section">
        <WardenDashboard refreshKey={refreshKey} />
      </section>

      <section className="dashboard-section">
        <MyComplaints />
      </section>

      <section className="dashboard-section">
        <RaiseComplaint onComplaintAdded={refreshPage} />
      </section>
    </div>
  );
}

export default App;