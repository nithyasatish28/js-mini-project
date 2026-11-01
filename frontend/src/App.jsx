
import { useState, useEffect } from "react";

import EquipmentList from "./components/EquipmentList";
import MyBookings from "./components/MyBookings";
import AddEquipment from "./components/AddEquipment";
import "./App.css";

const API_URL = "http://127.0.0.1:8001";

function App() {
  const [equipment, setEquipment] = useState([]);
  const [bookings, setBookings] = useState([]);

  const [currentRollNo, setCurrentRollNo] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  
  async function apiRequest(url, options = {}) {
    let response;

    try {
      response = await fetch(API_URL + url, options);
    } catch (err) {
      throw new Error(
        "Cannot connect to backend. Check whether FastAPI is running on port 8001."
      );
    }

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Something went wrong.");
    }

    return data;
  }

  async function loadEquipment(type = "") {
    try {
      setLoading(true);
      setError("");

      let url = "/equipment";

      if (type !== "") {
        url += "?type=" + encodeURIComponent(type);
      }

      const data = await apiRequest(url);
      setEquipment(data);

    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadEquipment();
  }, []);

  async function changeService(id, currentStatus) {
    try {
      setError("");
      setMessage("");

      const newStatus = currentStatus === 1 ? 0 : 1;

      await apiRequest(`/equipment/${id}/service`, {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(newStatus)
      });

      setMessage("Service status updated successfully!");
      await loadEquipment();

    } catch (err) {
      setError(err.message);
    }
  }


  async function bookEquipment(equipmentId, rollNo, bookingDate) {
    try {
      setError("");
      setMessage("");

      await apiRequest("/bookings", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          equipment_id: equipmentId,
          roll_no: rollNo,
          booking_date: bookingDate
        })
      });

      setMessage("Equipment booked successfully!");

      await loadBookings(rollNo);
      await loadEquipment();

    } catch (err) {
      setError(err.message);
    }
  }

  async function loadBookings(rollNo) {
    try {
      setError("");
      setMessage("");

      setCurrentRollNo(rollNo);

      const data = await apiRequest(
        "/bookings?roll_no=" + encodeURIComponent(rollNo)
      );

      setBookings(data);

      if (data.length === 0) {
        setMessage("No active bookings found for this roll number.");
      }

    } catch (err) {
      setError(err.message);
      setBookings([]);
    }
  }

  async function cancelBooking(id) {
    try {
      setError("");
      setMessage("");

      await apiRequest(`/bookings/${id}/cancel`, {
        method: "PATCH"
      });

      setMessage("Booking cancelled successfully!");

      if (currentRollNo) {
        await loadBookings(currentRollNo);
      }

      await loadEquipment();

    } catch (err) {
      setError(err.message);
    }
  }

  async function addEquipment(name, type, labRoom) {
    try {
      setError("");
      setMessage("");

      await apiRequest("/equipment", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          name: name,
          type: type,
          lab_room: labRoom
        })
      });

      setMessage("Equipment added successfully!");

      await loadEquipment();

      return true;

    } catch (err) {
      setError(err.message);
      return false;
    }
  }

  return (
    <div className="app-container">

      <header className="header">
        <h1>Laboratory Equipment Booking System</h1>
        <p>Manage laboratory equipment and student bookings</p>
      </header>

      {message && (
        <div className="success-message">
          {message}
        </div>
      )}

      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      {/* Equipment section */}
      <EquipmentList
        equipment={equipment}
        onBook={bookEquipment}
        onChangeService={changeService}
        onFilter={loadEquipment}
        loading={loading}
      />

      {/* Student bookings */}
      <MyBookings
        bookings={bookings}
        onShow={loadBookings}
        onCancel={cancelBooking}
      />

      {/* Add new equipment */}
      <AddEquipment
        onAdd={addEquipment}
      />

      <footer>
        Laboratory Equipment Booking System
      </footer>

    </div>
  );
}

export default App;

