import { useState } from "react";

function Warden({ complaints, counts, apiUrl, onDone }) {
  const [notes, setNotes] = useState({});
  const [message, setMessage] = useState("");

  function changeNote(id, value) {
    setNotes({ ...notes, [id]: value });
  }

  function moveNext(id) {
    const note = notes[id] || "";

    fetch(apiUrl + "/complaints/" + id + "/status?note=" + encodeURIComponent(note), {
      method: "PATCH",
    })
      .then((response) => response.json().then((data) => ({ ok: response.ok, data })))
      .then((result) => {
        if (result.ok) {
          setMessage("");
          setNotes({ ...notes, [id]: "" });
          onDone();
        } else {
          setMessage(result.data.detail);
        }
      });
  }

  return (
    <div>
      <h2>Warden</h2>
      <p>Open: {counts.open} | In progress: {counts.in_progress} | Resolved: {counts.resolved}</p>
      <p>{message}</p>

      {complaints.map((c) => (
        <div key={c.id}>
          <p>Room {c.room_no} | {c.category} | Roll no: {c.roll_no}</p>
          <p>{c.description}</p>
          <p>Status: {c.status}</p>

          {c.status !== "resolved" && (
            <div>
              <input
                placeholder="Note"
                value={notes[c.id] || ""}
                onChange={(e) => changeNote(c.id, e.target.value)}
              />
              <button onClick={() => moveNext(c.id)}>Move to next status</button>
            </div>
          )}
        </div>
      ))}
    </div>
  );
}

export default Warden;