function PlantCard({plant}){
    return <>
        <h1>{plant.name}</h1>
        <p>{plant.type}</p>
        <p>{plant.location}</p>
    </>
}

export default PlantCard