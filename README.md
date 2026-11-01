# Team 26 · Umbrella-Sharing Stations

| Team | Partner 1 | Partner 2 | Project | Branch |
|---|---|---|---|---|
| 26 | Konduru Nanda Kishore Raju | — (working alone) | [Umbrella-Sharing Stations](https://github.com/nithyasatish28/js-mini-project/blob/main/5-umbrella-sharing-stations.md) | `team-26-umbrellas` |

**Your project:** [Umbrella-Sharing Stations](https://github.com/nithyasatish28/js-mini-project/blob/main/5-umbrella-sharing-stations.md). Read it fully before you start. Your code goes in `backend/` and `frontend/` on this branch.

**Every 3 hours:** update this file, then commit and push it with the message `Check-in Day 1 12:00` (your day and time). Your instructor reads this page on GitHub.

## 1. Who is doing what

Update your own row at every check-in.

| Day | Partner | What will you do? | Completed? | What are you going to work on next? | Stuck on? |
|---|---|---|---|---|---|
| Day 1 | Konduru Nanda Kishore Raju | Backend setup, database models and E1, E2, E3, E7, Installing all essencial packages and requirements for project | Yes | Borrow and Return API | no |
| Day 2 | Konduru Nanda Kishore Raju |E4, E5, E6, validation and Swagger testing and planned for front end and fixed errors  | yes |  React frontend and API integration| no  |
| Day 3 | Konduru Nanda Kishore Raju |React components, navigation, CSS and frontend integration  | Almost done  |designing an dlay out and final touch for Web front end checking and final outputs  |CSS layout and final UI verification  |

## 2. Endpoint tracker

Fill in the method and path from your PRD's endpoint table. Status: ✅ done · 🟡 in progress · ⬜ not started

| # | Method + path | Built | Rules checked in /docs | Connected to React | Who |
|---|---|---|---|---|---|
| E1 |  | ✅ | ✅ | ✅ | Raju |
| E2 |  | ✅ | ✅ | ✅ | Raju |
| E3 |  | ✅ | ✅ | ✅ |  Raju|
| E4 |  | ✅ | ✅ | ✅ | Raju |
| E5 |  | ✅ | ✅ | ✅ | Raju |
| E6 |  | ✅ | ✅ | ✅ | Raju |
| E7 |  | ✅ | ✅ | ✅ | Raju |

## 3. Frontend tracker

| Part (from section 5 of your PRD) | Shows the data | Buttons work | Shows API errors | Who |
|---|---|---|---|---|
| Stations | ✅ | ✅ | ✅ | Raju |
| My umbrella | ✅ | ✅ | ✅ | Nanda mKishore Raju |
| Add a station | ✅ | ✅ | ✅ | Raju |

## 4. Blockers and help needed

Frontend
connecting the both frontend and backend end and the connecting buttons

## 5. How to run our app

To run the project, start the backend first and then start the frontend in another terminal.


**Backend**

.\backend\.venv\Scripts\Activate.ps1
python -m pip install -r backend\requirements.txt
python -m uvicorn backend.main:app --reload --port 8001
To check the API endpoints, open http://localhost:8001/docs

**Frontend**

cd frontend
npm install
npm run dev

The frontend will run at http://localhost:5173.


Open the frontend at [http://localhost:5173]. The backend API is available at [http://localhost:8001/docs].

## 6. Proof of work

Save a screenshot of `/docs` or your app as `screenshot.png` in this branch. It shows here:

![Backend](docs/screenshots/backend-api.png)

![Frontend](docs/screenshots/frontend-dashboard.png)