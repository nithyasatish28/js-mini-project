function StationItem({stations , onBorrow , onDetails}){
    return(
        <li className = "stations" onClick={() => onDetails(stations.id)} >
            <h2>{stations.name}</h2>
            <p>{stations.capacity}</p>
            <p>{stations.location}</p>
            <p>{stations.free_slots}</p>
            <p>{stations.umbrellas_available}</p>

            {stations.available ?(
            <button onClick={() => onBorrow(stations.id)}>Add</button>
            
            ): (  <p>{sold_out}</p>)

            }
        </li>
    );
}
export default StationItem;
