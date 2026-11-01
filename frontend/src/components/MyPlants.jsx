function MyPlants({ plants, API_URL, rollNo, onUpdate }) {
  
  function water(id) {
    fetch(`${API_URL}/plants/${id}?roll_no=${rollNo}`, { method: "POST" })
      .then(res => res.json())
      .then(data => {
        if (data.detail) {
          console.error("Watering failed:", data.detail); 
        } else {
          onUpdate(); // Silently refreshes the screen
        }
      })
      .catch(error => {
        console.error("Network error:", error);
      });
  }

  function giveUp(id) {
    fetch(`${API_URL}/plants/${id}`, { method: "PATCH" })
      .then(res => res.json())
      .then(data => {
        if (data.detail) {
          console.error("Give up failed:", data.detail); 
        } else {
          onUpdate(); 
        }
      })
      .catch(error => {
        console.error("Network error:", error);
      });
  }

  return (
    <div>
      <h2>My Plants</h2>

      {plants.length === 0 ? (
        <p>No plants adopted yet.</p>
      ) : (
        <ul className="plants">
          {plants.map(p => {
            const waterings = p.waterings || [];
            
            return (
              <li key={p.id} className="plant">
                <h3>{p.name}</h3>

                <details open>
                  <summary>Watering History</summary>
                  <ul>
                    {waterings.length > 0 ? (
                      waterings.map((watering, index) => (
                        <li key={index}>
                          {watering.watered_on} by {watering.roll_no}
                        </li>
                      ))
                    ) : (
                      <li>No watering history yet.</li>
                    )}
                  </ul>
                </details>

                <button onClick={() => water(p.id)}>Water</button>
                <button onClick={() => giveUp(p.id)}>Give up</button>
              </li>
            );
          })}
        </ul>
      )}
    </div>
  );
}

export default MyPlants;
