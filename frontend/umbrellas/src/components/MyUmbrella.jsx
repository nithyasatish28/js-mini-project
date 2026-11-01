import { useState } from "react";

function MyUmbrella({ API_URL, stations, handleResult, setMessage }) {
  const [rollNo, setRollNo] = useState("");
  const [umbrella, setUmbrella] = useState(null);
  const [stationId, setStationId] = useState("");

  function showUmbrella() {
    fetch(API_URL + "/students/" + rollNo + "/umbrella")
      .then((response) => response.json())
      .then((data) => {
        if (data.detail) {
          setMessage(data.detail);
          setUmbrella(null);
        } else {
        //   setMessage("");
          setUmbrella(data);
        }
      });
  }

  function returnUmbrella() {
    fetch(API_URL + "/borrows/" + umbrella.borrow_id + "/return?station_id=" + stationId, {
      method: "PATCH",
    })
      .then((response) => response.json())
      .then((data) => {
        handleResult(data, "Umbrella returned");
        // was their a error
        if (!data.detail) {
          setUmbrella(null);
        }
      });
  }

  return (
    <>
      <h2>My umbrella</h2>
      <input placeholder="Roll number" value={rollNo} onChange={(event) => setRollNo(event.target.value)} />
      <button onClick={showUmbrella}>Show</button>

      {umbrella ? (
        <div>
          <p>Borrowed from: {umbrella.station_name}</p>
          <select value={stationId} onChange={(event) => setStationId(event.target.value)}>
            <option value="">Choose a station</option>
            {/* first dropdown choice */}
            {stations.map((s) => (
              <option key={s.id} value={s.id}>{s.name}</option>
            //   1 choice for 1 station
            ))}
          </select>
          <button onClick={returnUmbrella}>Return</button>
        </div>
      ) : (
        <p></p>
      )}
    </>
  );
}

export default MyUmbrella;