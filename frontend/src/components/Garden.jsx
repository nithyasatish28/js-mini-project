import PlantCard from "./PlantCard.jsx";

function Garden({plants}){
    return <>
        {plants.map((plant) => <PlantCard key={plant.id} plant={plant}/>)}
    </>

}

export default Garden