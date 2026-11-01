import PlantCard from "./PlantCard"
const API_URL = "http://127.0.0.1:8001";

function MyPlants({plants,adopted_by,setPlants}){
 const filteredPlants = plants.filter(
    (plant) => plant.adopted_by === adopted_by
  
  );
function handleWater(plantId) {
  fetch(API_URL + "/water", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ plant_id: plantId, roll_no: adopted_by })
  })
    .then((response) => response.json())
    .then(() => {
      return fetch(API_URL + "/plants"); // fetching the updated list of plants
    })
    .then((response) => response.json())
    .then((data) => setPlants(data))
  }
function handleGiveUp(plantId) {
  fetch(API_URL + `/plants/${plantId}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ adopted_by: null })
  })
    .then((response) => response.json())
    .then(() => {
      return fetch(API_URL + "/plants");// fetching the updated list of plants

    })
    .then((response) => response.json())
    .then((data) => setPlants(data))
  }
  return (
    <>
    <h2>Adopted Plants for Roll No: {adopted_by}</h2>
    {filteredPlants.length > 0 ? (filteredPlants.map((fplant)=>(
        <><PlantCard key={fplant.id + "plant"} plant={fplant} setPlant={setPlants}/>
          <button key={fplant.id + "water"} onClick={() => handleWater(fplant.id)} >Water</button>
          <button key={fplant.id + "give up"} onClick={() => handleGiveUp(fplant.id)} >Give up</button>
        </>

    ))):(<p>No plants</p>)}
    </>
  );
}

export default MyPlants