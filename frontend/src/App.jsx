import { useState, useEffect } from "react";
import Warden from "./components/Warden";
import MyComplaints from "./components/MyComplaints";
import RaiseComplaint from "./components/RaiseComplaint";

const API_URL = "http://127.0.0.1:8001";

function App() {
  const [complaints, setComplaints] = useState([]);
  const [counts, setCounts] = useState({ open: 0, in_progress: 0, resolved: 0 });

  function loadComplaints() {
    fetch(API_URL + "/complaints")
      .then((response) => response.json())
      .then((data) => setComplaints(data));

    fetch(API_URL + "/stats")
      .then((response) => response.json())
      .then((data) => setCounts(data));
  }

  useEffect(() => {
    loadComplaints();
  }, []);

  return (
    <>
      <h1>Hostel Complaint Tracker</h1>
      <Warden complaints={complaints} counts={counts} />
      <RaiseComplaint />
      <MyComplaints />
    </>
  );
}

export default App;