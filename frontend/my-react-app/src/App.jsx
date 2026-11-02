import { useState } from "react";
import Navbar from "./components/Navbar";
import EventList from "./components/EventList";
import MyRegistrations from "./components/MyRegistrations";
import AddEvent from "./components/AddEvent";

function App() {
  const [activeTab, setActiveTab] = useState("all");
  const [refresh, setRefresh] = useState(0);

  function handleUpdate() {
    setRefresh((prev) => prev + 1);
  }

  return (
    <div>
      <Navbar activeTab={activeTab} setActiveTab={setActiveTab} />

      {/* Part 1: Events */}
      {(activeTab === "all" || activeTab === "events") && (
        <EventList refresh={refresh} onUpdate={handleUpdate} />
      )}

      {/* Part 2: My Events / Registrations */}
      {(activeTab === "all" || activeTab === "registrations") && (
        <MyRegistrations onUpdate={handleUpdate} />
      )}

      {/* Part 3: Add an Event */}
      {(activeTab === "all" || activeTab === "add") && (
        <AddEvent onUpdate={handleUpdate} />
      )}
    </div>
  );
}

export default App;
