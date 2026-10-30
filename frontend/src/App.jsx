import { useState, useEffect } from "react";
import WardenDashboard from "./components/WardenDashboard";
import MyComplaints from "./components/MyComplaints";
import RaiseComplaint from "./components/RaiseComplaint";

import "./App.css";

const API_URL = "http://127.0.0.1:8001";

function App() {
  const [complaints, setComplaints] = useState([]);
  const [stats, setStats] = useState({
    open: 0,
    in_progress: 0,
    resolved: 0,
  });

  const [error, setError] = useState("");
  const [refreshKey, setRefreshKey] = useState(0);

  // Helper function to handle API responses
  async function handleResponse(response) {
    const data = await response.json();

    if (!response.ok) {
      throw new Error(
        typeof data.detail === "string"
          ? data.detail
          : JSON.stringify(data.detail || "Something went wrong")
      );
    }

    return data;
  }

  // E1: Get all complaints
  async function getAllComplaints(status = "", category = "") {
    const params = new URLSearchParams();

    if (status) params.append("status", status);
    if (category) params.append("category", category);

    const response = await fetch(
      `${API_URL}/complaints?${params.toString()}`
    );

    return handleResponse(response);
  }

  // E2: Get one complaint with its updates
  async function getComplaint(id) {
    const response = await fetch(`${API_URL}/complaints/${id}`);

    return handleResponse(response);
  }

  // E3: Add a complaint
  async function addComplaint(formData) {
    const response = await fetch(`${API_URL}/complaints`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(formData),
    });

    const data = await handleResponse(response);
    refreshData();

    return data;
  }

  // E4: Move complaint to next status
  async function updateStatus(id, status, note) {
    const response = await fetch(
      `${API_URL}/complaints/${id}/status`,
      {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ status, note }),
      }
    );

    const data = await handleResponse(response);
    refreshData();

    return data;
  }

  // E5: Get complaints by roll number
  async function getStudentComplaints(rollNo) {
    const response = await fetch(
      `${API_URL}/students/${encodeURIComponent(rollNo)}/complaints`
    );

    return handleResponse(response);
  }

  // E6: Delete a complaint
  async function deleteComplaint(id) {
    const response = await fetch(`${API_URL}/complaints/${id}`, {
      method: "DELETE",
    });

    // Supports either 204 No Content or a JSON success response
    const data =
      response.status === 204
        ? null
        : await handleResponse(response);

    if (response.status === 204 && !response.ok) {
      throw new Error("Failed to delete complaint");
    }

    refreshData();
    return data;
  }

  // E7: Get complaint statistics
  async function getStats() {
    const response = await fetch(`${API_URL}/complaints/stats`);

    return handleResponse(response);
  }

  // Tell components to reload their data
  function refreshData() {
    setRefreshKey((previous) => previous + 1);
  }

  // Load complaints and stats
  useEffect(() => {
    async function loadData() {
      try {
        const [complaintData, statsData] = await Promise.all([
          getAllComplaints(),
          getStats(),
        ]);

        setComplaints(complaintData);
        setStats(statsData);
        setError("");
      } catch (err) {
        setError(err.message);
      }
    }

    loadData();
  }, [refreshKey]);

  return (
    <div className="app">
      <header>
        <h1>Hostel Complaint Tracker</h1>
        <p>Report, manage and track hostel complaints</p>
      </header>

      {error && <p className="error">{error}</p>}

      <WardenDashboard
        complaints={complaints}
        stats={stats}
        getAllComplaints={getAllComplaints}
        updateStatus={updateStatus}
        refreshKey={refreshKey}
      />

      <MyComplaints
        getStudentComplaints={getStudentComplaints}
        getComplaint={getComplaint}
        deleteComplaint={deleteComplaint}
        refreshKey={refreshKey}
      />

      <RaiseComplaint addComplaint={addComplaint} />
    </div>
  );
}

export default App;