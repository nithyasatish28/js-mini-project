import PlantCard from "./PlantCard.jsx";

function Garden({plants,setPlants}){
    return <div className="Garden">
    <h1>Garden</h1>
        {plants.map((plant) => <PlantCard key={plant.id} plant={plant} setPlants={setPlants}/>)}
    </div>

}

export default Garden;