
import{useState , useEffect} from "react";
import StationList from "./components/StationList";

const API_URL = "http://127.0.0.1:8001";

function App(){

  const [stations , setStations] = useState([]);
  // we can reload data
  const [Available , setAvailable] = useState({station:[],total:0});
 
 useEffect(()=>{
 fetch(API_URL + "/stations")
 .then((response) => response.json())
 .then((data) => setStations(data )) ;

 fetch(API_URL + "/available")
  .then((response) = response.json())
  .then((data) => setAvailable(data));
 } , []);

function  umbrellasAvailable(id){
  fetch(API_URL = "/Available/add"+id+"/1" , {
  
  })
  .then((response) => response.json())
  .then((data) => setAvailable(data));
}

return(
  <>
  <p> {Available.items.length}</p>
  <StationList stations={stations} onRefresh={umbrellasAvailable}/>
  </>
);
}
export default App;



// import{useState , useEffect} from "react";
// import StationList from "./components/StationList";

// const API_URL = "http://127.0.0.1:8001";

// function App(){

//   const [stations , setStations] = useState([]);
//   // we can reload data
//   const [Available , setAvailable] = useState({station:[],total:0});
 
//  useEffect(()=>{
//  fetch(API_URL + "/stations")
//  .then((response) => response.json())
//  .then((data) => setStations(data )) ;

//  fetch(API_URL + "/available")
//   .then((response) = response.json())
//   .then((data) => setAvailable(data));
//  } , []);

// function  umbrellasAvailable(id){
//   fetch(API_URL = "/Available/add"+id+"/1" , {
  
//   })
//   .then((response) => response.json())
//   .then((data) => setAvailable(data));
// }

// return(
//   <>
//   <p> {Available.items.length}</p>
//   <StationList stations={stations} onRefresh={umbrellasAvailable}/>
//   </>
// );
// }
// export default App;




import { useState, useEffect } from "react"; // useState = remember values, useEffect = run code when page loads
import StationList from "./components/StationList"; // the list component

const API_URL = "http://127.0.0.1:8001"; // backend address, written only here

function callApi(path, options) { // helper: calls the backend and throws the backend's error message
  return fetch(API_URL + path, { headers: { "Content-Type": "application/json" }, ...options }) // send request
    .then((response) => // when the reply arrives
      response.json().then((data) => { // read its JSON
        if (!response.ok) { // status 404 / 409 / 422
          throw new Error(data.detail); // use the backend's message
        }
        return data; // success: return the data
      })
    );
}

function App() { // the whole page

  const [stations, setStations] = useState([]); // stations shown in the list
  const [allStations, setAllStations] = useState([]); // all stations (for the Return dropdown)
  const [showAttention, setShowAttention] = useState(false); // true = only empty/full stations
  const [rollNo, setRollNo] = useState(""); // roll number used for Borrow
  const [selected, setSelected] = useState(null); // station details after a click
  const [myRoll, setMyRoll] = useState(""); // roll number used for My umbrella
  const [myBorrow, setMyBorrow] = useState(null); // my unreturned umbrella
  const [returnId, setReturnId] = useState(""); // station picked to return to
  const [form, setForm] = useState({ name: "", location: "", capacity: "", umbrellas_available: "" }); // add-station form
  const [error, setError] = useState(""); // backend error to show on the page

  function loadStations(attention) { // reload the lists from the backend
    const path = attention ? "/stations/attention" : "/stations"; // E7 or E1
    callApi(path).then((data) => setStations(data)).catch((e) => setError(e.message)); // list on screen
    callApi("/stations").then((data) => setAllStations(data)).catch((e) => setError(e.message)); // dropdown list
  }

  useEffect(() => { // runs when the page opens and when the Needs attention button is toggled
    loadStations(showAttention); // load the right list
  }, [showAttention]); // run again if showAttention changes

  function refreshMine() { // keep My umbrella up to date after any action
    if (myBorrow) { // only if one is showing
      callApi("/borrows/active/" + myRoll).then((data) => setMyBorrow(data)).catch(() => setMyBorrow(null)); // E6
    }
  }

  function afterAction() { // run after every successful action
    setError(""); // clear old error
    setSelected(null); // close old details
    loadStations(showAttention); // reload stations (no page refresh)
    refreshMine(); // reload my umbrella
  }

  function borrowUmbrella(id) { // E4: Borrow button
    callApi("/stations/" + id + "/borrow", { method: "POST", body: JSON.stringify({ roll_no: rollNo }) }) // POST
      .then(() => afterAction()) // success
      .catch((e) => setError(e.message)); // show backend message
  }

  function showDetails(id) { // E2: card click
    callApi("/stations/" + id).then((data) => setSelected(data)).catch((e) => setError(e.message)); // store details
  }

  function showMine() { // E6: Show button
    callApi("/borrows/active/" + myRoll)
      .then((data) => { setMyBorrow(data); setError(""); }) // show my umbrella
      .catch((e) => { setMyBorrow(null); setError(e.message); }); // nothing found
  }

  function returnUmbrella() { // E5: Return button
    callApi("/borrows/" + myBorrow.id + "/return", { method: "PATCH", body: JSON.stringify({ station_id: Number(returnId) }) }) // PATCH
      .then(() => { setMyBorrow(null); afterAction(); }) // hide umbrella and reload
      .catch((e) => setError(e.message)); // show backend message
  }

  function addStation() { // E3: Add station button
    callApi("/stations", {
      method: "POST", // POST
      body: JSON.stringify({
        name: form.name, // text
        location: form.location, // text
        capacity: Number(form.capacity), // text -> number
        umbrellas_available: Number(form.umbrellas_available), // text -> number
      }),
    })
      .then(() => { setForm({ name: "", location: "", capacity: "", umbrellas_available: "" }); afterAction(); }) // clear form, reload
      .catch((e) => setError(e.message)); // show backend message
  }

  function changeForm(e) { // typing in the add-station form
    setForm({ ...form, [e.target.name]: e.target.value }); // update only the typed field
  }

  return (
    <>
      {/* red error message from the backend */}
      {error && <p style={{ color: "red" }}>{error}</p>}

      {/* roll number for borrowing */}
      <input placeholder="Roll number" value={rollNo} onChange={(e) => setRollNo(e.target.value)} />
      {/* toggle all stations / needs attention */}
      <button onClick={() => setShowAttention(!showAttention)}>
        {showAttention ? "Show all" : "Needs attention"}
      </button>

      {/* the list of stations */}
      <StationList stations={stations} onBorrow={borrowUmbrella} onDetails={showDetails} />

      {/* details after clicking a card */}
      {selected && <pre>{JSON.stringify(selected, null, 2)}</pre>}

      <h2>My umbrella</h2>
      {/* roll number to look up */}
      <input placeholder="Roll number" value={myRoll} onChange={(e) => setMyRoll(e.target.value)} />
      <button onClick={showMine}>Show</button>
      {/* only when the student holds an umbrella */}
      {myBorrow && (
        <div>
          <p>Borrowed from {myBorrow.from_station_name} on {myBorrow.borrowed_on}</p>
          {/* dropdown to choose the return station */}
          <select value={returnId} onChange={(e) => setReturnId(e.target.value)}>
            <option value="">Pick a station</option>
            {allStations.map((s) => (
              <option key={s.id} value={s.id}>{s.name}</option>
            ))}
          </select>
          <button onClick={returnUmbrella}>Return</button>
        </div>
      )}

      <h2>Add a station</h2>
      <input name="name" placeholder="Name" value={form.name} onChange={changeForm} />
      <input name="location" placeholder="Location" value={form.location} onChange={changeForm} />
      <input name="capacity" placeholder="Capacity (1-30)" value={form.capacity} onChange={changeForm} />
      <input name="umbrellas_available" placeholder="Starting umbrellas" value={form.umbrellas_available} onChange={changeForm} />
      <button onClick={addStation}>Add station</button>
    </>
  );
}

export default App; // main.jsx imports this
