import { useState } from "react";

function MyEvents({ registrations, onShow, onCancel }) {
  const [rollNo, setRollNo] = useState("");

  return (
    <>
      <h1>My events</h1>
      <input placeholder="Your roll number" value={rollNo} onChange={(e) => setRollNo(e.target.value)} />
      <button onClick={() => onShow(rollNo)}>Show</button>
      <ul>
        {registrations.map((registration) => (
          <li key={registration.registration_id}>
            {registration.title} · {registration.event_date}
            <button onClick={() => onCancel(registration.registration_id, rollNo)}>Cancel</button>
          </li>
        ))}
      </ul>
    </>
  );
}

export default MyEvents;