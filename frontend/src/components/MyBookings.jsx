import { useState } from "react";

function MyBookings({ API_URL }) {
const [rollNo, setRollNo] = useState("");
const [bookings, setBookings] = useState([]);
const [message, setMessage] = useState("");

// E6 - Show student bookings
function showBookings() {
if (rollNo === "") {
setMessage("Please enter your roll number.");
return;
}


fetch(API_URL + "/bookings/student/" + rollNo)
  .then((response) => response.json())
  .then((data) => {
    setBookings(data);

    if (data.length === 0) {
      setMessage("No active bookings found.");
    } else {
      setMessage("");
    }
  });


}

// E7 - Cancel booking
function cancelBooking(id) {
fetch(API_URL + "/booking/" + id + "/cancel", {
method: "PATCH"
})
.then((response) => response.json())
.then((data) => {
setMessage(data.message);
showBookings();
});
}

return ( <section> <h2>My Bookings</h2>


  <label>
    Roll number{" "}
    <input
      type="text"
      value={rollNo}
      onChange={(event) => setRollNo(event.target.value)}
    />
  </label>

  <button onClick={showBookings}>Show</button>

  <p>{message}</p>

  {bookings.map((booking) => (
    <div key={booking.id}>
      <p>Equipment: {booking.equipment_name}</p>
      <p>Booking date: {booking.booking_date}</p>

      <button onClick={() => cancelBooking(booking.id)}>
        Cancel
      </button>
    </div>
  ))}
</section>


);
}

export default MyBookings;