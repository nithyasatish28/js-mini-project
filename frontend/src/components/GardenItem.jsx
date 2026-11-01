function GardenItem({ plant,onAdopt}) {
    // const [type, setType] = useState("");

  return (
    <li className="product">
        <h2>Name: {plant.name}</h2>
        <p>Type: {plant.type}</p>
        <p>Location: {plant.location}</p> 
        <p>Adopted_by: {plant.adopted_by || "Nobody" }</p>  
        <p>Last Watered :{plant.last_watered || "Not watered"}</p>
        <p>Need_water :{plant.need_water ? "True" : "False"}</p>              
        {plant.adopted_by === null && (
        <button onClick={() => onAdopt(plant.id)}>Adopt</button>)}  
    </li>
  );
}

export default GardenItem; 


