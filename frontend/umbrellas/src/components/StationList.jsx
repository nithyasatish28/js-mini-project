import { useState } from "react";
import StationItem from "./StationItem";
function StationList({ API_URL, stations, handleResult }) {
  const [rollNo, setRollNo] = useState("");
  const [attention, setAttention] = useState(null);
  const [details, setDetails] = useState(null);
  function onBorrow(id) {
    fetch(API_URL + "/borrow?roll_no=" + rollNo + "&station_id=" + id, {
      method: "POST",
    })
      .then((response) => response.json())
      .then((data) => {
        handleResult(data, "Umbrella borrowed");
        // Switches the page back to showing all stations
        setAttention(null);
      });
  }
   function onDetails(id) {
    fetch(API_URL + "/stations/" + id)
      .then((response) => response.json())
      .then((data) => setDetails(data));
  }
  function showAttention() {
    fetch(API_URL + "/stations/needs-attention")
      .then((response) => response.json())
      .then((data) => setAttention(data));
  }
  const listToShow = 
  attention === null ? 
  stations : attention;
//   if yes all station else which station needs attention.
  return (
    <>
      <h2>Stations</h2>
      <input placeholder="Roll number" 
    //   box is empty
      value={rollNo} 
    // what is in rollno  
    onChange={(r) => setRollNo(r.target.value)} />
      <button onClick={showAttention}>Needs attention</button>
      {/* passing with no value */}
      <button onClick={() => setAttention(null)}>Show all</button>
      {/* calling fun with value  */}
     {details ? <p>Details: {details.name}, capacity {details.capacity}</p> : <p></p>}
      <ol>
        {listToShow.map((station) => (
          <StationItem key={station.id} station={station} onBorrow={onBorrow} onDetails={onDetails} />
        ))}
      </ol>

    </>
  );
}

export default StationList;