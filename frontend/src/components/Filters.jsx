function Filters({ counts, onStatus, onCategory }) {
  return (
    <>
      <h2>Complaint Count</h2>
      <p>
        🔴 Open: {counts.open} | 🟡 In progress: {counts.in_progress} | 🟢 Resolved: {counts.resolved}
      </p>

      <h2>Filters</h2>
      <p>
        Status: <select onChange={(e) => onStatus(e.target.value)}>
          <option value="">All</option>
          <option value="open">Open</option>
          <option value="in_progress">In progress</option>
          <option value="resolved">Resolved</option>
        </select>
      </p>
      <p>
        Category: <select onChange={(e) => onCategory(e.target.value)}>
          <option value="">All</option>
          <option value="electrical">Electrical</option>
          <option value="plumbing">Plumbing</option>
          <option value="furniture">Furniture</option>
          <option value="cleaning">Cleaning</option>
          <option value="internet">Internet</option>
        </select>
      </p>
    </>
  );
}

export default Filters;