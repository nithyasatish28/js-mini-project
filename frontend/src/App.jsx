import { useState, useEffect } from "react";
import ComplaintList from "./components/ComplaintList";
import Filters from "./components/Filters";
import StudentSearch from "./components/StudentSearch";
import RaiseForm from "./components/RaiseForm";

const API_URL = "http://127.0.0.1:8001";

function App() {
  const [complaints, setComplaints] = useState([]);
  const [counts, setCounts] = useState({ open: 0, in_progress: 0, resolved: 0 });
  const [status, setStatus] = useState("");
  const [category, setCategory] = useState("");
  const [message, setMessage] = useState("");
  const [selected, setSelected] = useState({ updates: [] });

  // E1 and E7 bec they both need all complaints (E1 to show all complaints, and E7 to count each complaint)
  useEffect(() => {
    loadComplaints("", "");
  }, []);

  function loadComplaints(newStatus, newCategory) {
    setStatus(newStatus);
    setCategory(newCategory);

    // runs the get methond form /complaints endpoint for E1
    fetch(API_URL + "/complaints?status=" + newStatus + "&category=" + newCategory)
      .then((response) => response.json())
      .then((data) => setComplaints(data));

    // runs get method from /counts endpoint for E7
    fetch(API_URL + "/counts")
      .then((response) => response.json())
      .then((data) => setCounts(data));
  }

    // for E1 and E7 it reloads the list and counts with the new status and the category that's already picked
  function chooseStatus(name) {
    loadComplaints(name, category);
  }

  // same as chooseStatus, but picking a category button keeps the current status
  function chooseCategory(name) {
    loadComplaints(status, name);
  }

  // E2 gets one complaint and its updates, saved in selected for the Updates section
  function showUpdates(id) {
    // runs get method from /complaints/{id} endpoint
    fetch(API_URL + "/complaints/" + id)
      .then((response) => response.json())
      .then((data) => setSelected(data));
  }

    // E3 raises a new complaint, it starts as open 
  function addComplaint(roll_no, room_no, newCategory, description) {
    // runs post method from /complaints endpoint, the complaint details go in the url like the cart in the sample
    fetch(API_URL + "/complaints?roll_no=" + roll_no + "&room_no=" + room_no + "&category=" + newCategory + "&description=" + description, {method: "POST"})
      .then((response) => response.json())
      .then((data) => setMessage(data.detail))
      .then(() => loadComplaints(status, category));
  }

   // E4 patching the status and making it move to the next one
  function moveForward(id, note) {
    // runs patch method from /complaints/{id} endpoint
    fetch(API_URL + "/complaints/" + id + "?note=" + note, {method: "PATCH"})
      .then((response) => response.json())
      .then((data) => setMessage(data.detail)) // empty when it worked, the error when it didn't???
      .then(() => loadComplaints(status, category));
  }

  // E5 gets complaint based on roll no
  function showStudent(roll_no) {
    // runs get method from /students/{roll_no}/complaints endpoints
    fetch(API_URL + "/students/" + roll_no + "/complaints")
      .then((response) => response.json())
      .then((data) => setComplaints(data));
  }


  // E6 deleting compalaint 
  function deleteComplaint(id) {
    // runs delete method from /complaints/{id} endpoint to delete by id
    fetch(API_URL + "/complaints/" + id, {method: "DELETE"})
      .then((response) => response.json())
      .then((data) => setMessage(data.detail))
      .then(() => loadComplaints(status, category));
  }

    return (
    <>
      <p><b>{message}</b></p>
      <Filters counts={counts} onStatus={chooseStatus} onCategory={chooseCategory} />
      <StudentSearch onStudent={showStudent} />
      <ComplaintList
        complaints={complaints}
        onSelect={showUpdates}
        onMove={moveForward}
        onDelete={deleteComplaint}
      />
      <h2>Updates</h2>
      <p><strong>Complaint:</strong> {selected.description}</p>
      <ul>
        {selected.updates.map((update) => (
          <li key={update.id}>
            <strong>{update.status}</strong> - {update.note} ({update.updated_on.slice(0, 10)})
          </li>
        ))}
      </ul>
      <RaiseForm onAdd={addComplaint} />
    </>
  );
}

export default App;