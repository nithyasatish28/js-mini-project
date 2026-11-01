
import { useEffect, useState } from "react";
import { getPlants } from "./services/plantApi";
import "./App.css";

function App() {
    const [plants, setPlants] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        async function fetchPlants() {
            try {
                const data = await getPlants();
                setPlants(data);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        }

        fetchPlants();
    }, []);

    return (
        <div className="app">
            <h1>Plant Adoption</h1>
            <p>Welcome to our plant adoption website!</p>

            {loading && <p>Loading plants...</p>}

            {error && <p>{error}</p>}

            <div className="plant-list">
                {plants.map((plant) => (
                    <div className="plant-card" key={plant.id}>
                        <h2>{plant.name}</h2>
                        <p>Type: {plant.type}</p>
                        <p>Location: {plant.location}</p>
                        <p>
                            Water every {plant.water_every_days} days
                        </p>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default App;
