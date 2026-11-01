# Team 11 · Hostel Complaint Tracker

| Team | Partner 1 | Partner 2 | Project | Branch |
|---|---|---|---|---|
| 11 | Melvin Jacob | Naman Choudhary | [Hostel Complaint Tracker](https://github.com/nithyasatish28/js-mini-project/blob/main/1-hostel-complaint-tracker.md) | `team-11-hostel` |

---

## Problem Statement

Campus hostel management requires a transparent and efficient way to track and resolve student issues. This project builds a full-stack **Hostel Complaint Tracker** using a **FastAPI + SQLite** backend and a **React (Vite)** frontend:
- **Students** can raise a complaint for their room across 5 standard categories (`electrical`, `plumbing`, `furniture`, `cleaning`, `internet`) using their roll number, and track the progress of their complaints and update notes.
- **The Hostel Warden** manages all complaints on a dedicated dashboard: viewing status counts (`open`, `in_progress`, `resolved`), filtering by category and status, and transitioning complaints forward as work gets completed (`open` → `in_progress` → `resolved`).
- All actions update seamlessly in the React UI without requiring manual page reloads.

---

## Who Built What

### Melvin Jacob
- **Backend Models:** Created the `updates` table (`class updates(Base)`).
- **Backend Functions (`functions.py`):**
  - `create_complaint`: Inserts a new complaint into the database.
  - `delete_complaint`: Deletes an open complaint and its associated history logs.
  - `get_complaint_status_counts`: Aggregates and returns complaint counts grouped by status.
- **Frontend Components:**
  - `RaiseComplaint.jsx`: Form for students to submit a complaint with category buttons and validation.
  - `Warden.jsx`: Warden dashboard with real-time status counts, status/category filter buttons, and complaint status updates.

### Naman Choudhary
- **Backend Models:** Created the `complaints` table (`class complaints(Base)`).
- **Backend Functions (`functions.py`):**
  - `get_complaints`: Retrieves all complaints with optional filtering by status and category.
  - `get_one_complaint`: Retrieves a single complaint along with its complete update history.
  - `update_complaint_status`: Advances complaint status and logs the transition in the updates table.
  - `get_students_complaints_byrollno`: Retrieves all complaints associated with a specific roll number.
- **Frontend Components & Layout:**
  - `App.jsx`: Master layout, state coordination, and refresh communication between components.
  - `Complaints.jsx`: "My Complaints" component with roll number lookup, accordion details view, and delete capability.
  - `index.css`: Page styling, responsive layout, button styling, and badge classes.

---

## 1. Who is doing what (Progress Report)

| Day | Partner | What will you do? | Completed? | What are you going to work on next? | Stuck on? |
|---|---|---|---|---|---|
| Day 1 | Melvin Jacob | Created `updates` table model; built `create_complaint`, `delete_complaint`, and `get_complaint_status_counts` backend functions | ✅ Yes | Start frontend components | None |
| Day 1 | Naman Choudhary | Created `complaints` table model; built `get_complaints`, `get_one_complaint`, `update_complaint_status`, and `get_students_complaints_byrollno` backend functions | ✅ Yes | Connect API endpoints | None |
| Day 2 | Melvin Jacob | Built `RaiseComplaint.jsx` and `Warden.jsx` frontend components; hooked up POST, PATCH, and GET endpoints | ✅ Yes | Polish UI and filter behavior | None |
| Day 2 | Naman Choudhary | Built `App.jsx`, `Complaints.jsx`, and configured application layout and styling in `index.css` | ✅ Yes | Test component interactions | None |
| Day 3 | Melvin Jacob | Refined `Warden.jsx` filters and `RaiseComplaint.jsx` form inputs; verified end-to-end status transitions and counts | ✅ Yes | Final demo prep and testing | None |
| Day 3 | Naman Choudhary | Polished `Complaints.jsx` list display, accordion updates view, and delete functionality; verified responsive layout | ✅ Yes | Final demo prep and testing | None |

---

## 2. Endpoint tracker

Status: ✅ done · 🟡 in progress · ⬜ not started

| # | Method + path | Built | Rules checked in /docs | Connected to React | Who |
|---|---|---|---|---|---|
| E1 | `GET /complaints` | ✅ | ✅ | ✅ | Naman |
| E2 | `GET /complaints/{id}` | ✅ | ✅ | ✅ | Naman |
| E3 | `POST /complaints` | ✅ | ✅ | ✅ | Melvin |
| E4 | `PATCH /complaints/{complaint_id}` | ✅ | ✅ | ✅ | Naman |
| E5 | `GET /complaints/student/{rollno}` | ✅ | ✅ | ✅ | Naman |
| E6 | `DELETE /complaints/{id}` | ✅ | ✅ | ✅ | Melvin |
| E7 | `GET /complaints/stats/counts` | ✅ | ✅ | ✅ | Melvin |

---

## 3. Frontend tracker

| Part (from section 5 of your PRD) | Shows the data | Buttons work | Connected to API | Who |
|---|---|---|---|---|
| Warden | ✅ | ✅ | ✅ | Melvin |
| My complaints | ✅ | ✅ | ✅ | Naman |
| Raise a complaint | ✅ | ✅ | ✅ | Melvin |

---

## 4. Blockers and help needed

- None! All 7 API endpoints, business rules, and React frontend components are fully functional and verified.

---

## 5. How to run our app

### Backend (FastAPI)

1. Open a terminal and navigate to the `backend` folder:
   ```bash
   cd backend
   ```
2. Activate your virtual environment (if using one):
   ```bash
   # On Windows PowerShell:
   .venv\Scripts\Activate.ps1
   ```
3. Start the FastAPI server on port 8001:
   ```bash
   uvicorn main:app --reload --port 8001
   ```
4. Access the interactive API documentation at:
   - [http://localhost:8001/docs](http://localhost:8001/docs)

### Frontend (React + Vite)

1. Open a second terminal and navigate to the `frontend` folder:
   ```bash
   cd frontend
   ```
2. Install dependencies (if not already installed):
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```
4. Open your browser and navigate to the displayed URL (typically [http://localhost:5173](http://localhost:5173)).

---

## 6. Proof of work

![Our app](screenshot.png)
