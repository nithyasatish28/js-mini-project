import { useState } from "react";

function MyEvents() {
  const [rollNo, setRollNo] = useState("");

  function findEvents() {
    alert("Searching events for " + rollNo);
  }

  return (
    <>
      <h2>My Registered Events</h2>

      <input
        type="text"
        placeholder="Enter your roll number"
        value={rollNo}
        onChange={(e) => setRollNo(e.target.value)}
      />

      <button onClick={findEvents}>
        View My Events
      </button>
    </>
  );
}

export default MyEvents;