function BookEquipment() {
  const [rollNo, setRollNo] = useState("");
  const [bookingDate, setBookingDate] = useState("");
  const [message, setMessage] = useState("");

  function bookItem(id) {
    fetch( + "/bookings", {
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
        }
      });
  }

  return (
    <div>
      <h2>Book Equipment</h2>

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

      <button onClick={() => bookItem(item.id)}>
        Book
      </button>

      <p>{message}</p>
    </div>
  );
}
