function AddStation({ onStationAdded }) {
  async function addStation(event) {
    event.preventDefault();

    const station = {
      name: event.target.name.value,
      location: event.target.location.value,
      capacity: Number(event.target.capacity.value),
      umbrellas_available: Number(event.target.umbrellas_available.value)
    };

    const response = await fetch("http://127.0.0.1:8001/stations", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(station)
    });

    const data = await response.json();

    if (!response.ok) {
      alert(data.detail);
      return;
    }

    event.target.reset();
    onStationAdded();
  }

  return (
    <form onSubmit={addStation}>
      <h2>Add Station</h2>
      <input name="name" placeholder="Station name" required />
      <input name="location" placeholder="Location" required />
      <input name="capacity" type="number" placeholder="Capacity" min="1" max="30" required />
      <input name="umbrellas_available" type="number" placeholder="Umbrellas" min="0" required />
      <button type="submit">Add Station</button>
    </form>
  );
}

export default AddStation;