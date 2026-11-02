import { useState, useEffect } from "react";
import { getData } from "../services/api";
import StationItem from "./StationItem";

function StationList({ refresh }) {
  const [stations, setStations] = useState([]);

  useEffect(() => {
    getData("/stations")
      .then((data) => setStations(data))
      .catch((error) => console.log(error.message));
  }, [refresh]);

  return (
    <div>
      <h2>Umbrella Stations</h2>

      <div className="stations">
        {stations.map((station) => (
          <StationItem key={station.id} station={station} />
        ))}
      </div>
    </div>
  );
}

export default StationList;