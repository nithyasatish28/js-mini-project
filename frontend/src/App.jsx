import { useEffect, useState } from "react";
import EquipmentList from "./components/EquipmentList";
import MyBookings from "./components/MyBookings";
import AddEquipment from "./components/AddEquipment";

const API_URL = "http://127.0.0.1:8001";

async function fetchJson(url, options) {
  const response = await fetch(url, options);
  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail ?? `Request failed (${response.status})`);
  }

  return data;
}

function getDateString(date) {
  const localDate = new Date(
    date.getTime() - date.getTimezoneOffset() * 60000,
  );
  return localDate.toISOString().slice(0, 10);
}

function App() {
  const [equipment, setEquipment] = useState([]);
  const [equipmentType, setEquipmentType] = useState("");
  const [bookingDate, setBookingDate] = useState(getDateString(new Date()));
  const [rollNo, setRollNo] = useState("");
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");

  useEffect(() => {
    const url = equipmentType
      ? `${API_URL}/equipment/type/${encodeURIComponent(equipmentType)}`
      : `${API_URL}/equipment`;

    fetchJson(url)
      .then(setEquipment)
      .catch((requestError) => setError(requestError.message));
  }, [equipmentType]);


  // Reload equipment after adding new equipment
  function loadEquipment() {
    fetchJson(API_URL + "/equipment")
      .then(setEquipment)
      .catch((requestError) => setError(requestError.message));
  }

  function changeEquipmentStatus(equipment_id, in_service) {
    const query = new URLSearchParams({ in_service: String(in_service) });

    fetchJson(`${API_URL}/equipment/${equipment_id}/status?${query}`, {
      method: "PUT",
    })
      .then(() => {
        setEquipment((currentEquipment) =>
          currentEquipment.map((equipment) =>
            equipment.id === equipment_id
              ? { ...equipment, in_service }
              : equipment,
          ),
        );
        setError("");
        setMessage("Equipment status updated successfully.");
      })
      .catch((requestError) => {
        setMessage("");
        setError(requestError.message);
      });
  }

  function bookEquipment(equipment_id) {
    if (!rollNo.trim() || !bookingDate) {
      setMessage("");
      setError("Enter a roll number and booking date.");
      return;
    }

    const query = new URLSearchParams({
      equipment_id: String(equipment_id),
      roll_no: rollNo.trim(),
      booking_date: bookingDate,
    });

    fetchJson(`${API_URL}/booking?${query}`, { method: "POST" })
      .then(() => {
        setError("");
        setMessage("Equipment booked successfully.");
      })
      .catch((requestError) => {
        setMessage("");
        setError(requestError.message);
      });
  }

  const maxBookingDate = new Date();
  maxBookingDate.setDate(maxBookingDate.getDate() + 7);

  return (
    <main className="page-shell">
      <h1>Lab equipment</h1>

      <AddEquipment
        API_URL={API_URL}
        onEquipmentAdded={loadEquipment}
      />

      <MyBookings API_URL={API_URL} />

      <label>
        Equipment type{" "}
        <select
          value={equipmentType}
          onChange={(event) => setEquipmentType(event.target.value)}
        >
          <option value="">All equipment</option>
          <option value="microscope">Microscope</option>
          <option value="oscilloscope">Oscilloscope</option>
          <option value="3d-printer">3D printer</option>
          <option value="laptop">Laptop</option>
          <option value="camera">Camera</option>
        </select>
      </label>

      <p>
        <label>
          Booking date{" "}
          <input
            type="date"
            min={getDateString(new Date())}
            max={getDateString(maxBookingDate)}
            value={bookingDate}
            onChange={(event) => setBookingDate(event.target.value)}
          />
        </label>
        {"  "}
        <label>
          Roll number{" "}
          <input
            type="text"
            value={rollNo}
            onChange={(event) => setRollNo(event.target.value)}
          />
        </label>
      </p>

      {error && <p role="alert">{error}</p>}
      {message && <p role="status">{message}</p>}

      <EquipmentList
        equipment={equipment}
        onBook={bookEquipment}
        onChangeStatus={changeEquipmentStatus}
      />
    </main>
  );
}

export default App;