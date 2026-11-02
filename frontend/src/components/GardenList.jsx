import { useState} from "react";

import GardenItem from "./GardenItem";

function GardenList({ plants ,API_URL ,setPlants, onAdopt , rollNo }) {
    const [type, setType] = useState("");

    function filtertype(){
        let api_url = API_URL +"/plants";

        if(type !== ""){
            api_url = API_URL+ "/plants?type=" + type;
        }

        fetch(api_url).then(response => response.json().then((data) => setPlants(data)));

    }
    
    function Needwater(){
        fetch(API_URL + "/plants/needs-water").then((response) => response.json()).then((data) => setPlants(data));
    }


    function adopt(id){
     fetch(API_URL+"/plants/"+id+"/" + rollNo, 
        {method: "PATCH",}) 
      .then((response) => response.json())
      .then(() => onAdopt());      
    
    }
    
    function adoptable(){
        fetch(API_URL +"/plants").then((response)=>response.json()).then((data)=>setPlants(data.filter((plant)=> plant.adopted_by == null)))
    }
  return (
    <>
      <h1>Garden</h1>
      <ul  className="plants">
        <label>Filter by Type</label>
        <select value={type} onChange={(t) => setType(t.target.value)}>
          <option value="">ALL</option>
          <option value="flowering">flowering</option>
          <option value="herb">Herb</option>
          <option value="succulent">Succulent</option>
            <option value="indoor">indoor</option>
          <option value="tree">tree</option>        
        </select>
        <button onClick={(filtertype)}>FITER TYPEE</button>
        <button onClick={(Needwater)}>needs water today</button>
        <button onClick={(adoptable)}>Adopt</button>  
                     
        {plants.map((plant) => (
          <GardenItem key={plant.id} plant = {plant} onAdopt ={adopt} />
        ))}
       </ul>
      
    </>
  );    

}
export default GardenList;
