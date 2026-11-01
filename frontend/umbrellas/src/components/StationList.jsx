import StationItem from "./StationItem";

function StationList({ stations, onAdd }) {
  return (
    <>
      <h1>Umbrella Stations</h1>
      <ul className="stations">
        {stations.map((station) => (
          <StationItem key={station.id} station={station} onAdd={onAdd} />
        ))}
      </ul>
    </>
  );
}

export default StationList;