import { useState } from "react";

function EquipmentItem({ item, onBook, onChangeService }) {

  const [rollNo, setRollNo] = useState("");
  const [bookingDate, setBookingDate] = useState("");

  function handleBook() {
    if (!rollNo.trim() || !bookingDate) {
      alert("Please enter roll number and booking date.");
      return;
    }

    onBook(item.id, rollNo, bookingDate);
  }

  return (
    <div className="equipment-card">

      <div className="card-top">
        <h3>{item.name}</h3>

        {item.in_service === 0 && (
          <span className="out-label">
            Out of service
          </span>
        )}
      </div>

      <p><strong>Type:</strong> {item.type}</p>
      <p><strong>Room:</strong> {item.lab_room}</p>

      <div className="input-group">
        <label>Roll Number</label>

        <input
          type="text"
          placeholder="Enter roll number"
          value={rollNo}
          onChange={(e) => setRollNo(e.target.value)}
        />
      </div>

      <div className="input-group">
        <label>Booking Date</label>

        <input
          type="date"
          value={bookingDate}
          onChange={(e) => setBookingDate(e.target.value)}
        />
      </div>

      <button
        className="primary-btn"
        onClick={handleBook}
        disabled={item.in_service === 0}
      >
        Book Equipment
      </button>

      <button
        className="secondary-btn"
        onClick={() => onChangeService(item.id, item.in_service)}
      >
        {item.in_service === 1
          ? "Out of service"
          : "In service"}
      </button>

    </div>
  );
}

export default EquipmentItem;