function Navbar({ activeTab, setActiveTab }) {
  return (
    <nav>
      <h2>Campus Event Registration</h2>

      <button
        className={activeTab === "all" ? "active" : ""}
        onClick={() => setActiveTab("all")}
      >
        All Parts
      </button>

      <button
        className={activeTab === "events" ? "active" : ""}
        onClick={() => setActiveTab("events")}
      >
        Events
      </button>

      <button
        className={activeTab === "registrations" ? "active" : ""}
        onClick={() => setActiveTab("registrations")}
      >
        My Registrations
      </button>

      <button
        className={activeTab === "add" ? "active" : ""}
        onClick={() => setActiveTab("add")}
      >
        Add Event
      </button>
    </nav>
  );
}

export default Navbar;
