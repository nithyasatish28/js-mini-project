import { useState } from "react";

function StudentSearch({ onStudent }) {
  const [rollNo, setRollNo] = useState("");

  function show() {
    if (rollNo === "") {
      return;
    }
    onStudent(rollNo);
  }

  return (
    <>
      <h2>My complaints</h2>
      <input value={rollNo} onChange={(e) => setRollNo(e.target.value)} placeholder="Roll number" />
      <button onClick={show}>Show</button>
    </>
  );
}

export default StudentSearch;