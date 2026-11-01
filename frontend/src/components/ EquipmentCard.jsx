import { useState } from "react";

function EquipmentCard({ item, apiUrl, onRefresh }) {
  const [date, setDate] = useState("");
  const [rollNo, setRollNo] = useState("");
  const [error, setError] = useState("");
  const [msg, setMsg] = useState("");

  function handleBook() {
    setError("");
    setMsg("");
    if (!date || !rollNo) {
      setError("Enter a date and roll number.");
      return;
    }
    fetch(
      `${apiUrl}/booking?equipment_id=${item.id}&booking_date=${date}&roll_no=${rollNo}`,
      { method: "POST" }
    )
      .then((res) => res.json())
      .then((data) => {
        if (data.detail) {
          setError(data.detail);
        } else {
          setMsg("Booked!");
          setDate("");
          setRollNo("");
          onRefresh();
        }
      });
  }

  function handleToggle() {
    setError("");
    setMsg("");
    const newVal = item.in_service ? "false" : "true";
    fetch(`${apiUrl}/equipments/${item.id}/status?in_service=${newVal}`, {
      method: "PATCH",
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.detail && !data.message) {
          setError(data.detail);
        } else {
          onRefresh();
        }
      });
  }

  return (
    <li className="equipment-card">
      <h3>{item.name}</h3>
      <p>Type: {item.type} | Room: {item.lab_room}</p>
      {!item.in_service && <span className="badge">Out of service</span>}

      <div className="book-row">
        <input
          type="date"
          value={date}
          onChange={(e) => setDate(e.target.value)}
        />
        <input
          type="text"
          placeholder="Roll number"
          value={rollNo}
          onChange={(e) => setRollNo(e.target.value)}
        />
        <button className="btn-primary" onClick={handleBook}>Book</button>
      </div>

      {error && <p className="error">{error}</p>}
      {msg && <p className="success">{msg}</p>}
    </li>
  );
}

export default EquipmentCard;