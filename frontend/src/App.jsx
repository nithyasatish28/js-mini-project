import { useState, useEffect } from "react";
import Warden from "./components/Warden";
import MyComplaints from "./components/MyComplaints";
import RaiseComplaint from "./components/RaiseComplaint";

const API_URL = "http://127.0.0.1:8001";

function App() {
  const [complaints, setComplaints] = useState([]);
  const [counts, setCounts] = useState({ open: 0, in_progress: 0, resolved: 0 });
  const [complaint, setComplaint] = useState({});
  const [studentComplaints, setStudentComplaints] = useState([]);

  // E1: get all the complaints
  function getAllComplaints() {
    fetch(API_URL + "/complaints")
      .then((response) => response.json())
      .then((data) => setComplaints(data));
  }

  // E2: get one complaint by id, with its updates
  function getComplaint(id) {
    fetch(API_URL + "/complaints/" + id)
      .then((response) => response.json())
      .then((data) => setComplaint(data));
  }

  // E3: raise a complaint
  function raiseComplaint(rollno, roomno, category, description) {
    fetch(
      API_URL + "/complaints?rollno=" + rollno + "&roomno=" + roomno +
      "&category=" + category + "&description=" + description,
      { method: "POST" }
    )
      .then((response) => response.json())
      .then((data) => loadComplaints());
  }

  // E4: move a complaint to its next status, with a note
  function moveToNextStatus(id, note) {
    fetch(API_URL + "/complaints/" + id + "/status?note=" + note, { method: "PATCH" })
      .then((response) => response.json())
      .then((data) => loadComplaints());
  }

  // E5: get one student's complaints, by roll number
  function getStudentComplaints(rollNo) {
    fetch(API_URL + "/students/" + rollNo + "/complaints")
      .then((response) => response.json())
      .then((data) => setStudentComplaints(data));
  }

  // E6: delete a complaint (a successful delete sends back no body, so there is no .json())
  function deleteComplaint(id) {
    fetch(API_URL + "/complaints/" + id, { method: "DELETE" })
      .then((response) => loadComplaints());
  }

  // E7: get how many complaints there are in each status
  function getStatusCounts() {
    fetch(API_URL + "/stats")
      .then((response) => response.json())
      .then((data) => setCounts(data));
  }

  // reloads the list (E1) and the counts (E7)
  function loadComplaints() {
    getAllComplaints();
    getStatusCounts();
  }

  useEffect(() => {
    loadComplaints();
  }, []);

  return (
    <>
      <h1>Hostel Complaint Tracker</h1>
      <Warden complaints={complaints} counts={counts} apiUrl={API_URL} onDone={loadComplaints} />
      <RaiseComplaint apiUrl={API_URL} onDone={loadComplaints} />
<MyComplaints apiUrl={API_URL} onDone={loadComplaints} />
    </>
  );
}

export default App;