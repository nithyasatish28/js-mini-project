function AddPlant({ API_URL, onAdd }) {
  async function addPlant(formData) {
    const type = formData.get("type");

    const res = await fetch(API_URL + "/plants", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ type }),
    });

    if (res.ok) onAdd();
    else alert("Could not add plant");
  }

  return (
    <form action={addPlant}>
      <label>
        Type
        <select name="type" >
          <option value="" disabled>Select a plant type</option>
          <option value="flower">Flower</option>
          <option value="herb">Herb</option>
          <option value="succulent">Succulent</option>
          <option value="tree">Tree</option>
        </select>
      </label>
      <button type="submit">Add Plant</button>
    </form>
  );
}

export default AddPlant;