import { useState, useEffect } from "react";
import ComplaintList from "./components/ComplaintList";

const API_URL = "http://127.0.0.1:8001";

function App() {
  const [complaints, setComplaints] = useState([]);

  useEffect(() => {
    // GET /complaints
    fetch(API_URL + "/complaints")
      .then((response) => response.json())
      .then((data) => setComplaints(data));
  }, []);

  return (
    <>
      <h1>Hostel Complaint Tracker</h1>

      <ComplaintList complaints={complaints} />
    </>
  );
}

export default App