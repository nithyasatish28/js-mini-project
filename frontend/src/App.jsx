import { useState, useEffect } from "react";

import EquipmentList from "./components/EquipmentList";
import MyBookings from "./components/MyBookings";
import AddEquipment from "./components/AddEquipment";

const API_URL = "http://127.0.0.1:8001";

function App() {

  const [equipments, setEquipments] = useState([]);
  const [bookings, setBookings] = useState([]);
  const [message, setMessage] = useState("");

  // GET equipment
  function getEquipment(type = "") {

    let url = API_URL + "/equipment";

    if (type !== "") {
      url = API_URL + "/equipment/type/" + type;
    }

    fetch(url)
      .then((response) => response.json())
      .then((data) => {
        if (data.detail) {
          setMessage(data.detail);
        }
        else {
          setEquipments(data);
          setMessage("");
        }
      })
      .catch((error) => setMessage("Failed to fetch"));
  }

  // GET student bookings
  function showBookings(rollNo) {

    fetch(API_URL + "/students/" + rollNo + "/bookings")
      .then((response) => response.json())
      .then((data) => {
        if (data.detail) {
          setMessage(data.detail);
        }
        else {
          setBookings(data);
          setMessage(data.length === 0 ? "No bookings found" : "");
        }
      })
      .catch((error) => setMessage("Failed to fetch"));
  }

  // POST add equipment
  function addEquipment(name, equipmentType, labRoom) {

    fetch(API_URL + "/equipment?name=" + name + "&equipment_type=" + equipmentType + "&lab_room=" + labRoom, {
      method: "POST"
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.detail) {
          setMessage(data.detail);
        }
        else {
          setMessage("Equipment added successfully");
          getEquipment();
        }
      })
      .catch((error) => setMessage("Failed to fetch"));
  }

  // PATCH update service
  function toggleService(id, status) {

    fetch(API_URL + "/equipment/" + id + "?in_service=" + status, {
      method: "PATCH"
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.detail) {
          setMessage(data.detail);
        }
        else {
          setMessage("Equipment status updated");
          getEquipment();
        }
      })
      .catch((error) => setMessage("Failed to fetch"));
  }

  // POST book equipment
  function bookEquipment(id, rollNo, bookingDate) {

    fetch(API_URL + "/bookings?equipment_id=" + id + "&roll_no=" + rollNo + "&booking_date=" + bookingDate, {
      method: "POST"
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.detail) {
          setMessage(data.detail);
        }
        else {
          setMessage("Equipment booked successfully");
          showBookings(rollNo);
        }
      })
      .catch((error) => setMessage("Failed to fetch"));
  }

  // PATCH cancel booking
  function cancelBooking(id, rollNo) {

    fetch(API_URL + "/bookings/" + id + "/cancel", {
      method: "PATCH"
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.detail) {
          setMessage(data.detail);
        }
        else {
          setMessage("Booking cancelled successfully");
          showBookings(rollNo);
        }
      })
      .catch((error) => setMessage("Failed to fetch"));
  }

  useEffect(() => {
    getEquipment();
  }, []);

  return (
    <>
      <h1>Lab Equipment Booking System</h1>

      <p>{message}</p>

      <EquipmentList
        equipments={equipments}
        onBook={bookEquipment}
        onToggleService={toggleService}
        onFilter={getEquipment}
      />

      <hr />

      <MyBookings
        bookings={bookings}
        onShow={showBookings}
        onCancel={cancelBooking}
      />

      <hr />

      <AddEquipment onAdd={addEquipment} />
    </>
  );
}

export default App;