import PlantCard from "./PlantCard.jsx";

function Garden({plants}){
    return <>
    <h1>Garden</h1>
        {plants.map((plant) => <PlantCard key={plant.id} plant={plant}/>)}
    </>

}

export default Garden;