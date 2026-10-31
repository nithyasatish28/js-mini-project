import { useState } from "react";

export default function MyUmbrella({ stations, apiUrl, onError, onSuccess }) {
  const [rollNo, setRollNo] = useState("");
  const [activeBorrow, setActiveBorrow] = useState(null);
  const [selectedStationId, setSelectedStationId] = useState("");

  const handleCheckBorrow = async () => {
    if (!rollNo.trim()) {
      onError("Please enter a roll number.");
      return;
    }
    onError("");
    try {
      const res = await fetch(`${apiUrl}/borrows/active?roll_no=${rollNo.trim()}`);
      const data = await res.json();
      if (!res.ok) {
        setActiveBorrow(null);
        onError(data.detail || "No active umbrella found.");
      } else {
        setActiveBorrow(data);
      }
    } catch (err) {
      onError("Failed to fetch student status.");
    }
  };

  const handleReturn = async () => {
    if (!selectedStationId) {
      onError("Please select a return station.");
      return;
    }
    onError("");
    try {
      const res = await fetch(
        `${apiUrl}/borrows/${rollNo.trim()}/return?station_id=${selectedStationId}`,
        { method: "PATCH" }
      );
      const data = await res.json();
      if (!res.ok) {
        onError(data.detail || "Return failed.");
      } else {
        setActiveBorrow(null);
        setSelectedStationId("");
        onSuccess();
      }
    } catch (err) {
      onError("Error processing return.");
    }
  };

  return (
    <div className="section-block">
      <h2>My Umbrella</h2>
      <div className="form-inline">
        <input
          type="text"
          placeholder="Enter Roll No"
          value={rollNo}
          onChange={(e) => setRollNo(e.target.value)}
        />
        <button className="btn-primary" onClick={handleCheckBorrow}>Show</button>
      </div>

      {activeBorrow && (
        <div className="borrow-details-card">
          <p><strong>Roll No:</strong> {activeBorrow.roll_no}</p>
          <p><strong>Borrowed From:</strong> {activeBorrow.from_station_name}</p>
          
          <div className="form-inline" style={{ marginTop: "10px" }}>
            <select
              value={selectedStationId}
              onChange={(e) => setSelectedStationId(e.target.value)}
            >
              <option value="">Select Return Station</option>
              {stations.map((s) => (
                <option key={s.id} value={s.id}>
                  {s.name} ({s.capacity - s.umbrellas_available} free)
                </option>
              ))}
            </select>
            <button className="btn-primary" onClick={handleReturn}>Return</button>
          </div>
        </div>
      )}
    </div>
  );
}