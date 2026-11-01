import PlantCard from "./PlantCard.jsx";
import {useState} from "react";

function Garden({plants,setPlants}){
    const [type,setType] = useState("")
    let filteredPlants = [...plants]
    if (type !== ""){
        filteredPlants = filteredPlants.filter((plant) => plant.type === type)
    }

    function handleType(e) {    // function is an event handler used to update the component's state whenever someone types into the input field
        setType(e.target.value);

    }


    return <div className="Garden">
    <h1>Garden</h1>
        type:
        <select name="type" value={type} onChange={handleType}>
            <option value="">No Filter</option>
            <option value="succulent">succulent</option>
            <option value="flowering">flowering</option>
            <option value="herb">herb</option>
            <option value="indoor">indoor</option>
            <option value="tree">tree</option>
        </select>
        {filteredPlants.map((plant) => <PlantCard key={plant.id} plant={plant} setPlants={setPlants}/>)}
    </div>

}

export default Garden;