function AddPlant({ API_URL, onAdd }) {
  async function addPlant(e) {
    e.preventDefault(); // Stop the page from reloading

    // 1. Get values directly from the form inputs
    const form = e.target;
    const name = form.name.value;
    const type = form.type.value;
    const location = form.location.value;
    const days = form.water_every_days.value;

    // 2. Put them directly into the URL as query parameters
    const url = `${API_URL}/plants?name=${name}&type=${type}&location=${location}&water_every_days=${days}`;

    // 3. Send the POST request (no body, no headers needed)
    const res = await fetch(url, { method: "POST" });

    if (res.ok) {
      onAdd();       // Tell parent to refresh the list
      form.reset();  // Clear the form inputs
    } else {
      alert("Failed to add plant. Check console for details.");
    }
  }

  return (
    <form onSubmit={addPlant}>
      <label>
        <strong>Name:</strong>
        <input name="name" required />
      </label>
      <br /><br />
      
      <label>
        <strong>Type:</strong>
        <select name="type" required>
          <option value="flowering">Flowering</option>
          <option value="herb">Herb</option>
          <option value="succulent">Succulent</option>
          <option value="tree">Tree</option>
          <option value="indoor">Indoor</option>
        </select>
      </label>
      <br /><br />

      <label>
        <strong>Location:</strong>
        <input name="location" required />
      </label>
      <br /><br />

      <label>
        <strong>Water Every (Days):</strong>
        <input name="water_every_days" type="number" required />
      </label>
      <br /><br />

      <button type="submit">Add Plant</button>
    </form>
  );
}

export default AddPlant;
