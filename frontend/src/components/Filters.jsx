function Filters({ counts, onStatus, onCategory }) {
  return (
    <>
      <h2>Counts</h2>
      <p>
        🔴 Open: {counts.open} | 🟡 In progress: {counts.in_progress} | 🟢 Resolved: {counts.resolved}
      </p>

      <h2>Filter by status</h2>
      <button onClick={() => onStatus("")}>All</button>
      <button onClick={() => onStatus("open")}>Open</button>
      <button onClick={() => onStatus("in_progress")}>In progress</button>
      <button onClick={() => onStatus("resolved")}>Resolved</button>

      <h2>Filter by category</h2>
      <button onClick={() => onCategory("")}>All</button>
      <button onClick={() => onCategory("electrical")}>Electrical</button>
      <button onClick={() => onCategory("plumbing")}>Plumbing</button>
      <button onClick={() => onCategory("furniture")}>Furniture</button>
      <button onClick={() => onCategory("cleaning")}>Cleaning</button>
      <button onClick={() => onCategory("internet")}>Internet</button>
    </>
  );
}

export default Filters;