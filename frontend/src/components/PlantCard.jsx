import AdoptForm from "./AdoptForm.jsx";

function PlantCard({plant, setPlants}){
    let adopted = plant.adopted_by != null ? <p>Adopted by : {plant.adopted_by}</p> :<> <p>Orphaned</p> <AdoptForm plant={plant} setPlants={setPlants}/> </>

    return <><h2>{plant.name}</h2> <div className="Garden-plant">

        <p>type: {plant.type}</p>
        <p>location: {plant.location}</p>

        <p>last watered: {plant.last_watered != null ? plant.last_watered.watered_on : "Haven't yet"}</p>

        {adopted}


    </div> </>
}

export default PlantCard