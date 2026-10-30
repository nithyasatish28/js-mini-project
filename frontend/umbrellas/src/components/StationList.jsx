import StationItem from './StationItem';

function StationList ({stations , onBorrow , onDetails}) {
    return(
        <>
        {/* title */}
        <h1>Umbrella-Stations</h1>
        <ul className = "Stations">
            {stations.map((station)=>(
                <StationItem key={station.id} station={station} onBorrow={onBorrow} onDetails={onDetails}/>
            ))}    
                
                </ul>
                </>
    );
}

export default StationList ;