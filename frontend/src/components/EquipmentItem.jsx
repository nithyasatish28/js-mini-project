// One item from OUR API's GET /equipment:
// { id, name, type, lab_room, in_service }

import { useState } from "react";

function EquipmentItem({ equipment, onBook, onToggleService }) {

  const [showForm, setShowForm] = useState(false);
  const [rollNo, setRollNo] = useState("");
  const [bookingDate, setBookingDate] = useState("");

  function handleBooking() {
    if (!rollNo.trim() || !bookingDate) {
      return;
    }

    onBook(equipment.id, rollNo, bookingDate);
  }

  return (
    <li className="product">

      <h2>{equipment.name}</h2>
      <p>Type: {equipment.type}</p>
      <p>Lab Room: {equipment.lab_room}</p>

      {equipment.in_service === 0 && <p>Out of service</p>}

      {equipment.in_service === 1 ? (
        <button onClick={() => onToggleService(equipment.id, 0)}>
          Out of Service
        </button>
      ) : (
        <button onClick={() => onToggleService(equipment.id, 1)}>
          In Service
        </button>
      )}

      {equipment.in_service && (
        <button onClick={() => setShowForm(!showForm)}>
          Book
        </button>
      )}

      {showForm && (
        <>
          <h3>Book Equipment</h3>

          <input
            type="text"
            placeholder="Roll Number"
            value={rollNo}
            onChange={(e) => setRollNo(e.target.value)}
          />

          <input
            type="date"
            value={bookingDate}
            onChange={(e) => setBookingDate(e.target.value)}
          />

          <button onClick={handleBooking}>
            Confirm Booking
          </button>
        </>
      )}

    </li>
  );
}

export default EquipmentItem;