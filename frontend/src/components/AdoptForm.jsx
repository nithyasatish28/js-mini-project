import { useState } from 'react';

const API_URL = "http://127.0.0.1:8001";

function AdoptForm({plant,setPlants}) {
  const [RollNo, setRollNo] = useState("");

  function handleChange(e) {    // function is an event handler used to update the component's state whenever someone types into the input field
    setRollNo(e.target.value);

  }
  function adopt(RollNo){
      fetch(API_URL + `/plants/${plant.id}`, {
          method: "PATCH",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ adopted_by: RollNo + "" })
      })
          .then((response) => response.json())
          .then(() => {
              return fetch(API_URL + "/plants");// fetching the updated list of plants

          })
          .then((response) => response.json())
          .then((data) => setPlants(data))

  }

  function handleSubmit(e) {
    e.preventDefault(); // Prevents the page from refreshing on form submit
    adopt(RollNo); // Pass the current RollNo state up to the parent component
    
  }

  return (
    <form onSubmit={handleSubmit}>
      <label>Adopt:
        <input
          type="text" 
          value={RollNo}
          onChange={handleChange}
        />
      </label>
      <button type='submit'>Adopt</button>
    </form>
  )
}
 

export default AdoptForm;

