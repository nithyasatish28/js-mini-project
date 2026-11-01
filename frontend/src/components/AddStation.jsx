import { useState } from "react";

function AddStation({ apiUrl, onError, onStationAdded }) {
    const [name, setName] = useState("");
    const [location, setLocation] = useState("");
    const [capacity, setCapacity] = useState("");
    const [umbrellas, setUmbrellas] = useState("");

    async function handleSubmit(e) {
        e.preventDefault();
        onError("");

        const params = new URLSearchParams({
            name: name.trim(),
            location: location.trim(),
            capacity: capacity,
            umbrellas_available: umbrellas
        });

        try {
            const res = await fetch(`${apiUrl}/stations?${params}`, {
                method: "POST"
            });
            const data = await res.json();

            if (!res.ok) throw new Error(data.detail);

            alert("Station added successfully.");
            setName("");
            setLocation("");
            setCapacity("");
            setUmbrellas("");
            await onStationAdded();
        } catch (err) {
            onError(err.message);
        }
    }

    return (
        <div>
            <h2>Add Station</h2>
            <form onSubmit={handleSubmit}>
                <input type="text" placeholder="Station Name" value={name} onChange={e => setName(e.target.value)} required />
                <input type="text" placeholder="Location" value={location} onChange={e => setLocation(e.target.value)} required />
                <input type="number" placeholder="Capacity (1-30)" value={capacity} onChange={e => setCapacity(e.target.value)} min="1" max="30" required />
                <input type="number" placeholder="Available Umbrellas" value={umbrellas} onChange={e => setUmbrellas(e.target.value)} min="0" required />
                <button type="submit">Add Station</button>
            </form>
        </div>
    );
}

export default AddStation;