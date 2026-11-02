# Team 21 · Hostel Complaint Tracker

| Team | Partner 1 | Partner 2 | Project | Branch |
|---|---|---|---|---|
| 21 | Jiken Pulinbhai Jasoliya | Vilok | [Hostel Complaint Tracker](https://github.com/nithyasatish28/js-mini-project/blob/main/1-hostel-complaint-tracker.md) | `team-21-hostel` |

**Every 3 hours:** update this file, then commit and push it with the message `Check-in Day 1 12:00` (your day and time). Your instructor reads this page on GitHub.

## 1. Who is doing what

Update your own row at every check-in.

| Day | Partner | What will you do? | Completed? | What are you going to work on next? | Stuck on? |
|---|---|---|---|---|---|
| Day 1 | Jiken Pulinbhai Jasoliya | starting with the Backend (API) | not | Debugging | debugging |
| Day 1 | Vilok |  |  |  |  |
| Day 2 | Jiken Pulinbhai Jasoliya | debugging the backend APIs | yes | last checks |  |
| Day 2 | Vilok | started with the frontend | yes | last checks | nothing |
| Day 3 | Jiken Pulinbhai Jasoliya | last checks | yes | run the code | nope |
| Day 3 | Vilok |  |  |  |  |

## 2. Endpoint tracker

Fill in the method and path from your PRD's endpoint table. Status: ✅ done · 🟡 in progress · ⬜ not started

| # | Method + path | Built | Rules checked in /docs | Connected to React | Who |
|---|---|---|---|---|---|
| E1 | `GET /complaints` | ✅ | ✅ | ✅ |  |
| E2 | `GET /complaints/{complaint_id}` | ✅ | ✅ | ✅ |  |
| E3 | `POST /complaints` | ✅ | ✅ | ✅ |  |
| E4 | `PUT /complaints/{complaint_id}` | ✅ | ✅ | ✅ |  |
| E5 | `DELETE /complaints/{complaint_id}` | ✅ | ✅ | ✅ |  |
| E6 | `GET /complaints/status/{status}` | ✅ | ✅ | ✅ |  |
| E7 | `PATCH /complaints/{complaint_id}/resolve` | ✅ | ✅ | ✅ |  |

## 3. Frontend tracker

| Part (from section 5 of your PRD) | Shows the data | Buttons work | Shows API errors | Who |
|---|---|---|---|---|
| Warden dashboard and complaint management | ✅ | ✅ | ✅ |  |
| My complaints (roll number search) | ✅ | ✅ | ✅ |  |
| Raise a complaint | ✅ | ✅ | ✅ |  |

## 4. Blockers and help needed

- 

## 5. How to run our app

Fill this in by the end of Day 2. Someone who has never seen your code should be able to follow it.

**Backend**

```bash
cd backend
npm start
```

**Frontend**

```bash
cd frontend
npm install
npm run dev
```

The Node API uses the existing `backend/complaints.db`. To run the FastAPI implementation instead, run `python -m pip install -r requirements.txt` and then `python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000` from the backend folder.

## 6. Proof of work

Save a screenshot of `/docs` or your app as `screenshot.png` in this branch. It shows here:

![Our app](screenshot.png)
