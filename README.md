# Team 17 · Campus Event Registration

| Team | Partner 1 | Partner 2 | Project | Branch |
|---|---|---|---|---|
| 17 | Yashwant Gowda | S Mohammed Abrar ul Haq | [Campus Event Registration](https://github.com/nithyasatish28/js-mini-project/blob/main/2-campus-event-registration.md) | `team-17-events` |

**Every 3 hours:** update this file, then commit and push it with the message `Check-in Day 1 12:00` (your day and time). Your instructor reads this page on GitHub.

## 1. Who is doing what

Update your own row at every check-in.

| Day | Partner | What will you do? | Completed? | What are you going to work on next? | Stuck on? |
|---|---|---|---|---|---|
| Day 1 | Yashwant Gowda | Database setup & endpoints E1-E4 | ✅ Yes | Rule checks in /docs | None |
| Day 1 | S Mohammed Abrar ul Haq | Endpoints E5-E7 & SQLite tables | ✅ Yes | Rules validation & pytest | None |
| Day 2 | Yashwant Gowda | React UI components (Events, Cards, Filter) | ✅ Yes | Registration & cancel wiring | None |
| Day 2 | S Mohammed Abrar ul Haq | My Registrations, Add Event & on-page errors | ✅ Yes | End-to-end integration & styling | None |
| Day 3 | Yashwant Gowda | Testing, README documentation, demo rehearsal | ✅ Yes | Project submission | None |
| Day 3 | S Mohammed Abrar ul Haq | Code walkthrough preparation & live demo | ✅ Yes | Project submission | None |

## 2. Endpoint tracker

Fill in the method and path from your PRD's endpoint table. Status: ✅ done · 🟡 in progress · ⬜ not started

| # | Method + path | Built | Rules checked in /docs | Connected to React | Who |
|---|---|---|---|---|---|
| E1 | `GET /events` (optional `?category=...`) | ✅ | ✅ | ✅ | Yashwant Gowda |
| E2 | `GET /events/{event_id}` | ✅ | ✅ | ✅ | Yashwant Gowda |
| E3 | `POST /events` | ✅ | ✅ | ✅ | Yashwant Gowda |
| E4 | `DELETE /events/{event_id}` | ✅ | ✅ | ✅ | Yashwant Gowda |
| E5 | `POST /events/{event_id}/registrations` | ✅ | ✅ | ✅ | S Mohammed Abrar ul Haq |
| E6 | `GET /registrations/{roll_no}` | ✅ | ✅ | ✅ | S Mohammed Abrar ul Haq |
| E7 | `PATCH /registrations/{registration_id}/cancel` | ✅ | ✅ | ✅ | S Mohammed Abrar ul Haq |

## 3. Frontend tracker

| Part (from section 5 of your PRD) | Shows the data | Buttons work | Shows API errors | Who |
|---|---|---|---|---|
| Events | ✅ | ✅ | ✅ | Yashwant Gowda |
| My events | ✅ | ✅ | ✅ | S Mohammed Abrar ul Haq |
| Add an event | ✅ | ✅ | ✅ | Yashwant Gowda & S Mohammed Abrar ul Haq |

## 4. Blockers and help needed

- None. All 7 API endpoints, all validation rules, and all 3 frontend parts are fully implemented and passing.

## 5. How to run our app

Someone who has never seen your code should be able to follow it.

### Prerequisites
- Python 3.10+
- Node.js (v18+) & npm

### Backend

```bash
cd backend
python -m uvicorn main:app --port 8001 --reload
```

The backend server will run at `http://127.0.0.1:8001`.
You can view and test the interactive API documentation at:
- `http://127.0.0.1:8001/docs`

To run the automated rule tests:
```bash
cd backend
pytest test_main.py
```

### Frontend

```bash
cd frontend/my-react-app
npm install
npm run dev
```

Open your browser at the Vite URL shown (typically `http://localhost:5173` or `http://127.0.0.1:5173`).

## 6. Proof of work

Save a screenshot of `/docs` or your app as `screenshot.png` in this branch. It shows here:

![Our app](screenshot.png)
