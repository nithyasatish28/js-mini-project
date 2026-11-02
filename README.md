# Team 11 · Hostel Complaint Tracker

| Team | Partner 1 | Partner 2 | Project | Branch |
|---|---|---|---|---|
| 11 | Melvin Jacob | Naman Choudhary | [Hostel Complaint Tracker](https://github.com/nithyasatish28/js-mini-project/blob/main/1-hostel-complaint-tracker.md) | `team-11-hostel` |

---

## Problem Statement

Currently, hostel complaints are handled through physical paper registers, verbal complaints, or chaotic WhatsApp groups where messages constantly get buried, ignored, or forgotten.

This creates two big problems:

- Students have no transparency on whether anyone is actually fixing their issue.
- Wardens have no organized system to track pending work or filter issues by category.

Our project replaces that chaos with a centralized, real-time web portal.

We built a full-stack Hostel Complaint Tracker using FastAPI, SQLalchemy, and React.

- Students can raise room complaints across 5 categories using their roll number and follow real-time progress.
- Wardens get a dedicated dashboard with live status counts, multi-category filters, and a structured lifecycle transition: open 
→
→ in_progress 
→
→ resolved.

---

## Who Built What

### Melvin Jacob
- **Backend Models:** Created the `updates` table (`class updates(Base)`).
- **Backend Functions (`functions.py`):**
  - `create_complaint`: Inserts a new complaint into the database.
  - `delete_complaint`: Deletes an open complaint and its associated history logs.
  - `get_complaint_status_counts`: Aggregates and returns complaint counts grouped by status.
- **Frontend Components and Layout:**
  - `RaiseComplaint.jsx`: Form for students to submit a complaint with category buttons and validation.
   `Warden.jsx`: Warden control panel displaying  status , note inputs, and status advancement actions.

### Naman Choudhary
- **Backend Models:** Created the `complaints` table (`class complaints(Base)`).
- **Backend Functions (`functions.py`):**
  - `get_complaints`: Retrieves all complaints with optional filtering by status and category.
  - `get_one_complaint`: Retrieves a single complaint along with its complete update history.
  - `update_complaint_status`: Advances complaint status and logs the transition in the updates table.
  - `get_students_complaints_byrollno`: Retrieves all complaints associated with a specific roll number.
- **Frontend Components:**
  - `Complaints.jsx`: "My Complaints" component with roll number lookup, accordion details view, and delete capability.
  - `App.jsx`:State coordination, and refresh communication between components.
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


js-mini-project/
├── backend/
│   ├── main.py                     # FastAPI application endpoints and CORS configuration
│   ├── functions.py                # SQLAlchemy ORM models, session logic, and DB operations
│   └── hostel_complaint_tracker.db # SQLite relational database file
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── RaiseComplaint.jsx  # Student complaint submission form component
│   │   │   ├── Complaints.jsx      # Student lookup, accordion history, and cancellation
│   │   │   └── Warden.jsx          # Warden dashboard, metric counters, and status management
│   │   ├── App.jsx                 # Application root coordinating shared refresh state
│   │   ├── main.jsx                # DOM mounting point
│   │   └── index.css               # Global responsive styling and UI layout rules
│   ├── index.html                  # HTML entry point
│   ├── package.json                # Frontend package configuration and scripts
│   └── vite.config.js              # Vite build tool configuration
└── README.md                       # Project documentation


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