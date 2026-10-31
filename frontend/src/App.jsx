import { useState, useEffect } from "react";
<<<<<<< HEAD
// import Garden from "./components/Garden";
=======
import Garden from "./components/Garden";
>>>>>>> db392d3366bc646ca2cb9c6b3e0191172c1e1cc5
import MyPlants from "./components/MyPlants";
import AddPlant from "./components/AddPlant";

const API_URL = "http://127.0.0.1:8001";

function App() {
  const [plants, setPlants] = useState([]);
<<<<<<< HEAD
  const [rollNo, setRollNo] = useState("");
=======

  useEffect(() => {
    fetch(API_URL + "/plants")
      .then((res) => res.json())
      .then((data) => setPlants(data));
  }, []);
>>>>>>> db392d3366bc646ca2cb9c6b3e0191172c1e1cc5

  function refreshAll() {
    fetch(API_URL + "/plants")
      .then((res) => res.json())
      .then((data) => setPlants(data));
  }
<<<<<<< HEAD

  useEffect(() => {
    refreshAll();
  }, []);
=======
>>>>>>> db392d3366bc646ca2cb9c6b3e0191172c1e1cc5

  return (
    <div>
      <h1>Campus Garden</h1>
<<<<<<< HEAD


      <input
        placeholder="Enter your Roll No"
        value={rollNo}
        onChange={(e) => setRollNo(e.target.value)}
      />

      <AddPlant API_URL={API_URL} onAdd={refreshAll} />
      {/* <Garden plants={plants} API_URL={API_URL} onAdopt={refreshAll} /> */}
      <MyPlants plants={plants} API_URL={API_URL} rollNo={rollNo} onUpdate={refreshAll} />
=======
      <AddPlant API_URL={API_URL} onAdd={refreshAll} />
      <Garden plants={plants} API_URL={API_URL} onAdopt={refreshAll} />
      <MyPlants plants={plants} API_URL={API_URL} onUpdate={refreshAll} />
>>>>>>> db392d3366bc646ca2cb9c6b3e0191172c1e1cc5
    </div>
  );
}

export default App;