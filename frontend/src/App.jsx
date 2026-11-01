import { useState, useEffect } from "react";
// import Garden from "./components/GardenItem";
import GardenList from "./components/GardenList";
// import MyPlants from "./components/MyPlants";
// import AddPlant from "./components/AddPlant";

const API_URL = "http://127.0.0.1:8001";

function App() {
  const [plants, setPlants] = useState([]);
  const [rollNo, setRollNo] = useState(""); 

  function refreshAll() {
    fetch(API_URL + "/plants")
      .then((res) => res.json())
      .then((data) => setPlants(data));
  }

useEffect(() => {
  refreshAll();
}, []);

  return (
   
    <div>
      <h1>Campus Garden</h1>


      <input
        placeholder="Enter Roll No: AUXXUGXXX"
        value={rollNo}
        onChange={(e) => setRollNo(e.target.value)}
      />

      {/* <AddPlant API_URL={API_URL} onAdd={refreshAll} /> */}
      <GardenList plants={plants} API_URL={API_URL} setPlants={setPlants}  rollNo ={rollNo} onAdopt={refreshAll}/>
      {/* <MyPlants plants={plants} API_URL={API_URL} rollNo={rollNo} onUpdate={refreshAll} /> */}
    </div>
  );
}

export default App;