
import React, { useState, useEffect } from "react";

const API_URL = "http://127.0.0.1:8001";

function App() {

  const [equipment, setEquipment] = useState([]);
  const [bookings, setBookings] = useState([]);

  const [rollNo, setRollNo] = useState("");
  const [bookingDate, setBookingDate] = useState("");
  const [filterType, setFilterType] = useState("");

  const [name, setName] = useState("");
  const [type, setType] = useState("microscope");
  const [room, setRoom] = useState("");

  const [message, setMessage] = useState("");

  // Get all equipment
  function getEquipment() {
    fetch(API_URL + "/equipment")
      .then(response => response.json())
      .then(data => setEquipment(data));
  }

  // Load equipment when page opens
  useEffect(() => {
    getEquipment();
  }, []);

  // Filter equipment
  function filterEquipment(value) {
    setFilterType(value);

    let url = API_URL + "/equipment";

    if (value !== "") {
      url = url + "?type=" + value;
    }

    fetch(url)
      .then(response => response.json())
      .then(data => setEquipment(data));
  }

  // Book equipment
  function bookItem(id) {

    fetch(API_URL + "/bookings", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        equipment_id: id,
        roll_no: rollNo,
        booking_date: bookingDate
      })
    })
      .then(response => response.json())
      .then(data => {
        if (data.detail) {
          setMessage(data.detail);
        } else {
          setMessage("Equipment booked successfully!");
          getEquipment();
        }
      });
  }

  // Change service status
  function changeStatus(item) {

    fetch(API_URL + "/equipment/" + item.id + "/service", {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        in_service: item.in_service === 1 ? 0 : 1
      })
    })
      .then(response => response.json())
      .then(data => {
        if (data.detail) {
          setMessage(data.detail);
        } else {
          getEquipment();
          setMessage("Status updated!");
        }
      });
  }

  // Show student's bookings
  function showBookings() {

    fetch(API_URL + "/bookings/" + rollNo)
      .then(response => response.json())
      .then(data => {
        if (data.detail) {
          setMessage(data.detail);
          setBookings([]);
        } else {
          setBookings(data);
          setMessage("");
        }
      });
  }

  // Cancel booking
  function cancelBooking(id) {

    fetch(API_URL + "/bookings/" + id, {
      method: "DELETE"
    })
      .then(response => response.json())
      .then(data => {
        if (data.detail) {
          setMessage(data.detail);
        } else {
          setMessage("Booking cancelled!");
          showBookings();
          getEquipment();
        }
      });
  }

  // Add new equipment
  function addEquipment() {

    fetch(API_URL + "/equipment", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        name: name,
        type: type,
        lab_room: room
      })
    })
      .then(response => response.json())
      .then(data => {
        if (data.detail) {
          setMessage(data.detail);
        } else {
          setMessage("Equipment added successfully!");
          setName("");
          setRoom("");
          getEquipment();
        }
      });
  }

  return (
    <div>

      <h1>Lab Equipment Booking</h1>

      <p>{message}</p>

      {/* EQUIPMENT SECTION */}

      <h2>Available Equipment</h2>

      <select
        value={filterType}
        onChange={(e) => filterEquipment(e.target.value)}
      >
        <option value="">All Equipment</option>
        <option value="microscope">Microscope</option>
        <option value="oscilloscope">Oscilloscope</option>
        <option value="3d-printer">3D Printer</option>
        <option value="laptop">Laptop</option>
        <option value="camera">Camera</option>
      </select>

      <br /><br />

      <input
        type="text"
        placeholder="Enter Roll Number"
        value={rollNo}
        onChange={(e) => setRollNo(e.target.value)}
      />

      <input
        type="date"
        value={bookingDate}
        onChange={(e) => setBookingDate(e.target.value)}
      />

      <div>
        {equipment.map(item => (
          <div key={item.id}>

            <h3>{item.name}</h3>

            <p>Type: {item.type}</p>
            <p>Room: {item.lab_room}</p>

            {item.in_service === 0 &&
              <p>Out of service</p>
            }

            <button
              onClick={() => bookItem(item.id)}
              disabled={item.in_service === 0}
            >
              Book
            </button>

            <button onClick={() => changeStatus(item)}>
              {item.in_service === 1 ? "Out of service" : "In service"}
            </button>

            <hr />

          </div>
        ))}
      </div>

      {/* MY BOOKINGS SECTION */}

      <h2>My Bookings</h2>

      <input
        type="text"
        placeholder="Enter Roll Number"
        value={rollNo}
        onChange={(e) => setRollNo(e.target.value)}
      />

      <button onClick={showBookings}>
        Show Bookings
      </button>

      <div>
        {bookings.map(booking => (
          <div key={booking.id}>

            <p>Equipment: {booking.name}</p>
            <p>Date: {booking.booking_date}</p>

            <button onClick={() => cancelBooking(booking.id)}>
              Cancel
            </button>

            <hr />

          </div>
        ))}
      </div>

      {/* ADD EQUIPMENT SECTION */}

      <h2>Add Equipment</h2>

      <input
        type="text"
        placeholder="Equipment Name"
        value={name}
        onChange={(e) => setName(e.target.value)}
      />

      <br /><br />

      <select
        value={type}
        onChange={(e) => setType(e.target.value)}
      >
        <option value="microscope">Microscope</option>
        <option value="oscilloscope">Oscilloscope</option>
        <option value="3d-printer">3D Printer</option>
        <option value="laptop">Laptop</option>
        <option value="camera">Camera</option>
      </select>

      <br /><br />

      <input
        type="text"
        placeholder="Lab Room"
        value={room}
        onChange={(e) => setRoom(e.target.value)}
      />

      <br /><br />

      <button onClick={addEquipment}>
        Add Equipment
      </button>

    </div>
  );
}

export default App;
