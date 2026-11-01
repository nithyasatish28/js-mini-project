import { useState, useEffect } from "react";
import Warden from "./components/Warden";
import MyComplaints from "./components/MyComplaints";
import RaiseComplaint from "./components/RaiseComplaint";

const API_URL = "http://127.0.0.1:8001";

function App() {
  const [complaints, setComplaints] = useState([]);
  const [counts, setCounts] = useState({ open: 0, in_progress: 0, resolved: 0 });
  const [complaint, setComplaint] = useState({ updates: [] });
  const [studentComplaints, setStudentComplaints] = useState([]);
  const [wardenMessage, setWardenMessage] = useState("");
  const [raiseMessage, setRaiseMessage] = useState("");
  const [myMessage, setMyMessage] = useState("");

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
      .then((data) => {
        if (data.detail) {
          setMyMessage(data.detail);
        } else {
          setComplaint(data);
        }
      });
  }

  // E3: raise a complaint
  function raiseComplaint(rollno, roomno, category, description) {
    fetch(
      API_URL + "/complaints?rollno=" + rollno + "&roomno=" + roomno +
      "&category=" + category + "&description=" + description,
      { method: "POST" }
    )
      .then((response) => response.json())
      .then((data) => {
        if (data.detail) {
          setRaiseMessage(data.detail);
        } else {
          setRaiseMessage("Complaint raised");
          loadComplaints();
        }
      });
  }

  // E4: move a complaint to its next status, with a note
  function moveToNextStatus(id, note) {
    fetch(API_URL + "/complaints/" + id + "/status?note=" + note, { method: "PATCH" })
      .then((response) => response.json())
      .then((data) => {
        if (data.detail) {
          setWardenMessage(data.detail);
        } else {
          setWardenMessage("");
          loadComplaints();
        }
      });
  }

  // E5: get one student's complaints, by roll number
  function getStudentComplaints(rollNo) {
    if (rollNo === "") {
      setMyMessage("Enter a roll number");
    } else {
      fetch(API_URL + "/students/" + rollNo + "/complaints")
        .then((response) => response.json())
        .then((data) => {
          setMyMessage("");
          setStudentComplaints(data);
        });
    }
  }

  // E6: delete a complaint
  function deleteComplaint(id, rollNo) {
    fetch(API_URL + "/complaints/" + id, { method: "DELETE" })
      .then((response) => response.json())
      .then((data) => {
        if (data.detail) {
          setMyMessage(data.detail);
        } else {
          setMyMessage("");
          loadComplaints();
          getStudentComplaints(rollNo);
        }
      });
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
      <Warden
        complaints={complaints}
        counts={counts}
        message={wardenMessage}
        moveToNextStatus={moveToNextStatus}
      />
      <RaiseComplaint message={raiseMessage} raiseComplaint={raiseComplaint} />
      <MyComplaints
        studentComplaints={studentComplaints}
        complaint={complaint}
        message={myMessage}
        getStudentComplaints={getStudentComplaints}
        getComplaint={getComplaint}
        deleteComplaint={deleteComplaint}
      />
    </>
  );
}

export default App;