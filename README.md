# Team 16 · Hostel Complaint Tracker

| Team | Partner 1 | Partner 2 | Project | Branch |
|---|---|---|---|---|
| 16 | Samhita Bhuvanagiri | Aiman Patil | [Hostel Complaint Tracker](https://github.com/nithyasatish28/js-mini-project/blob/main/1-hostel-complaint-tracker.md) | `team-16-hostel` |

**Every 3 hours:** update this file, then commit and push it with the message `Check-in Day 1 12:00` (your day and time). Your instructor reads this page on GitHub.

## 1. Who is doing what

Update your own row at every check-in.

| Day | Partner | What will you do? | Completed? | What are you going to work on next? | Stuck on? |
|---|---|---|---|---|---|
| Day 1 | Samhita Bhuvanagiri | Main.py - Getting the API's to work and making sure they follow the rules and display correct error  | Yes | Frontend |  |
| Day 1 | Aiman Patil | Functions.py - created and connected the tables as well as defined function logic | Yes | Frontend |  |
| Day 2 | Samhita Bhuvanagiri | Finish the react connection in App.jsx so that the frontend can call the apis from backend | Yes | Some parts of the front end will probably be buggy after aiman makes the buttons and everything show up, so i'll debug the logic/code in App.jsx |  |
| Day 2 | Aiman Patil |  |  |  |  |
| Day 3 | Samhita Bhuvanagiri |  |  |  |  |
| Day 3 | Aiman Patil |  |  |  |  |

## 2. Endpoint tracker

Fill in the method and path from your PRD's endpoint table. Status: ✅ done · 🟡 in progress · ⬜ not started

| # | Method + path | Built | Rules checked in /docs | Connected to React | Who |
|---|---|---|---|---|---|
| E1 | GET/complaints | ✅ | ✅ | ✅ | function by aiman, api and react connection by sam |
| E2 | GET/complaints/{complaint_id}  | ✅ | ✅ | ✅ | function by aiman, api and react connection by sam |
| E3 | POST/complaints | ✅ | ✅ | ✅ | function by aiman, api and react connection by sam |
| E4 | PATCH/complaints/{complaint_id} | ✅ | ✅ | ✅ | function by aiman, api and react connection by sam |
| E5 | GET/students/{roll_no}/complaints | ✅ | ✅ | ✅ | function by aiman, api and react connection by sam |
| E6 | DELETE/complaints/{complaint_id} | ✅ | ✅ | ✅ | function by aiman, api and react connection by sam |
| E7 | GET/counts | ✅ | ✅ | ✅ | function by aiman, api and react connection by sam |

## 3. Frontend tracker

| Part (from section 5 of your PRD) | Shows the data | Buttons work | Shows API errors | Who |
|---|---|---|---|---|
| Warden | ⬜ | ⬜ | ⬜ |  |
| My complaints | ⬜ | ⬜ | ⬜ |  |
| Raise a complaint | ⬜ | ⬜ | ⬜ |  |

## 4. Blockers and help needed

- 

## 5. How to run our app

Fill this in by the end of Day 2. Someone who has never seen your code should be able to follow it.

**Backend**

## Backend (FastAPI + SQLite)

1. Open a bash terminal in the `backend/` folder:
   ```
   cd backend
   ```
2. Create and activate a virtual environment (optional):
   ```
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Install the requirements:
   ```
   pip install fastapi uvicorn sqlalchemy
   ```
4. Start the server on port 8001:
   ```
   uvicorn main:app --reload --port 8001
   ```
5. Open http://127.0.0.1:8001/docs to see and test all 7 endpoints.

Note:
- All the commands to be given in a bash terminal.
- The database file `hostel.db` is created automatically on the first run, and the data stays in it after restarting.
- The API only accepts requests from a frontend running at `http://localhost:5173` or `http://127.0.0.1:5173` (the default Vite address).

```

**Frontend**

```bash
cd frontend

```

## 6. Proof of work

Save a screenshot of `/docs` or your app as `screenshot.png` in this branch. It shows here:

![Our app](screenshot.png)
