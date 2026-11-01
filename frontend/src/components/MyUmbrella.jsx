import { useState } from "react";

function MyUmbrella({ stations, rollNo, apiUrl, onError, onSuccess }) {
    const [borrow, setBorrow] = useState(null);
    const [toStationId, setToStationId] = useState("");

    async function checkBorrow() {
        if (!rollNo.trim()) return onError("Enter your roll number.");
        onError("");

        try {
            const res = await fetch(`${apiUrl}/borrows/active/${encodeURIComponent(rollNo)}`);
            const data = await res.json();
            if (!res.ok) throw new Error(data.detail);
            setBorrow(data);
        } catch (err) {
            setBorrow(null);
            onError(err.message);
        }
    }

    async function returnUmbrella() {
        if (!toStationId) return onError("Select a return station.");
        onError("");

        try {
            const res = await fetch(
                `${apiUrl}/borrows/${borrow.borrow_id}/return?to_station_id=${toStationId}`,
                { method: "PATCH" }
            );
            const data = await res.json();
            if (!res.ok) throw new Error(data.detail);

            alert("Umbrella returned successfully.");
            setBorrow(null);
            setToStationId("");
            await onSuccess();
        } catch (err) {
            onError(err.message);
        }
    }

    return (
        <div>
            <h2>My Umbrella</h2>
            <button onClick={checkBorrow}>Check My Borrow</button>

            {borrow && (
                <div>
                    <p>Roll Number: {borrow.roll_no}</p>
                    <p>Borrow ID: {borrow.borrow_id}</p>
                    <p>From Station: {borrow.from_station_name}</p>
                    <p>Borrowed On: {borrow.borrowed_on}</p>

                    <label>Return Station: </label>
                    <select value={toStationId} onChange={e => setToStationId(e.target.value)}>
                        <option value="">Select Station</option>
                        {stations.map(station => (
                            <option key={station.id} value={station.id}>
                                {station.name}
                            </option>
                        ))}
                    </select>

                    <button onClick={returnUmbrella}>Return Umbrella</button>
                </div>
            )}
        </div>
    );
}

export default MyUmbrella;