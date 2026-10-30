import { useState, useEffect } from "react";
import Warden from "./components/Warden";
import MyComplaints from "./components/MyComplaints";
import RaiseComplaint from "./components/RaiseComplaint";

const API_URL = "http://127.0.0.1:8001";

function App() {
  const [complaints, setComplaints] = useState([]);

  function loadComplaints() {
    fetch(API_URL + "/complaints")
      .then((response) => response.json())
      .then((data) => setComplaints(data));
  }

  useEffect(() => {
    loadComplaints();
  }, []);

  return (
    <>
      <h1>Hostel Complaint Tracker</h1>
      <Warden complaints={complaints} />
      <RaiseComplaint />
      <MyComplaints />
    </>
  );
}

export default App;