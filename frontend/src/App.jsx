import { useState, useEffect } from "react";
import ComplaintList from "./components/ComplaintList";

const API_URL = "http://127.0.0.1:8001";

function App() {
  const [complaints, setComplaints] = useState([]);
  const [selected, setSelected] = useState({ updates: [] });

  useEffect(() => {
    //  uses GET /complaints from api
    fetch(API_URL + "/complaints")
      .then((response) => response.json())
      .then((data) => setComplaints(data));
  }, []);

  function showUpdates(id) {
    // uses GET /complaints/{id} from api 
    fetch(API_URL + "/complaints/" + id)
      .then((response) => response.json())
      .then((data) => setSelected(data));
  }

  return (
    <>
      <ComplaintList complaints={complaints} onSelect={showUpdates} />
      <h2>Updates</h2>
      <p>{selected.description}</p>
      <ul>
        {selected.updates.map((update) => (
          <li key={update.id}>
            <p>{update.status}</p>
            <p>{update.note}</p>
            <p>{update.updated_on}</p>
          </li>
        ))}
      </ul>
    </>
  );
}

export default App;