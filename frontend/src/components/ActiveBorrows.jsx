import React from "react";
import { useState, useEffect } from "react";

function ActiveBorrows({ apiUrl, refreshKey }) {
  const [borrows, setBorrows] = useState([]);
  const [loading, setLoading] = useState(true);

  // Fetch every umbrella that is currently out
  async function getBorrows() {
    try {
      const response = await fetch(`${apiUrl}/borrows/active`);
      const data = await response.json();

      setBorrows(data);
    } catch (error) {
      alert("Unable to load umbrella records.");
    }

    setLoading(false);
  }

  // Load on start, and again whenever refreshKey changes
  useEffect(() => {
    getBorrows();
  }, [refreshKey]);

  // Turn the time from the server into something easy to read
  function formatTime(timeString) {
    return new Date(timeString).toLocaleString();
  }

  return (
    <section className="station-section">
      <h2>Umbrellas Currently Out</h2>

      <button className="refresh-button" onClick={getBorrows}>
        Refresh
      </button>

      {loading ? (
        <p>Loading...</p>
      ) : borrows.length === 0 ? (
        <p>No umbrellas are currently out.</p>
      ) : (
        <table className="borrow-table">
          <thead>
            <tr>
              <th>Roll Number</th>
              <th>Umbrella</th>
              <th>Taken From</th>
              <th>Taken On</th>
            </tr>
          </thead>

          <tbody>
            {borrows.map((borrow) => (
              <tr key={borrow.borrow_id}>
                <td>{borrow.roll_no}</td>
                <td>#{borrow.borrow_id}</td>
                <td>{borrow.station_name}</td>
                <td>{formatTime(borrow.borrowed_on)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </section>
  );
}

export default ActiveBorrows;