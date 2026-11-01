# Team 03 · Lab Equipment Booking

| Team | Partner 1 | Partner 2 | Project | Branch |
|---|---|---|---|---|
| 03 | Afifa Adeen | Syed Kaifuddin | [Lab Equipment Booking](https://github.com/nithyasatish28/js-mini-project/blob/main/3-lab-equipment-booking.md) | `team-03-lab` |

**Every 3 hours:** update this file, then commit and push it with the message `Check-in Day 1 12:00` (your day and time). Your instructor reads this page on GitHub.

## 1. Who is doing what

Update your own row at every check-in.

| Day | Partner | What will you do?                    | Completed? | What are you going to work on next? | Stuck on? |
|---|---|--------------------------------------|------------|-------------------------------------|-----------|
| Day 1 | Afifa Adeen | database + E1, E2, E3                | Yes        | Frontend                            | No        |
| Day 1 | Syed Kaifuddin | E4, E5, E6, E7, readme               | Yes        | Frontend                            | No        |
| Day 2 | Afifa Adeen | App.jsx and AddEquipment component   |    Yes        | Testing                             |   No        |
| Day 2 | Syed Kaifuddin | EquipmentCard and Bookings component | Yes           |  Testing                                   |    No       |
| Day 3 | Afifa Adeen | Viva                                 |            |                                     |           |
| Day 3 | Syed Kaifuddin | Viva                                 |            |                                     |           |

## 2. Endpoint tracker

Fill in the method and path from your PRD's endpoint table. Status: ✅ done · 🟡 in progress · ⬜ not started

| # | Method + path | Built | Rules checked in /docs | Connected to React | Who   |
|---|---|---|---|---|-------|
| E1 |  | ✅ | ✅ | ✅ | afifa |
| E2 |  | ✅ | ✅ | ✅ | afifa |
| E3 |  | ✅ | ✅ | ✅ | afifa |
| E4 |  | ✅ | ✅ | ✅ | kaif  |
| E5 |  | ✅ | ✅ | ✅ | kaif  |
| E6 |  | ✅ | ✅ | ✅ | kaif  |
| E7 |  | ✅ | ✅ | ✅ | kaif  |

## 3. Frontend tracker

| Part (from section 5 of your PRD) | Shows the data | Buttons work | Shows API errors | Who   |
|---|---|---|---|-------|
| Equipment | ✅ | ✅ | ✅ | kaif  |
| My bookings | ✅ | ✅ | ✅ | kaif  |
| Add equipment | ✅ | ✅ | ✅ | afifa |

## 4. Blockers and help needed

- we had problem related to mismatch of the values from the api and values in the function which led to conflict.
- we also had issues in git pull cause uncommitted changes needs to be stashed but later when poped everything was overlapping. and led to conflict.

## 5. How to run our app

Fill this in by the end of Day 2. Someone who has never seen your code should be able to follow it.

**Backend**

```bash
cd backend
pip install uvicorn
uvicorn main:app --reload --port 8001

```

**Frontend**

```bash
cd frontend
npm install
npm run dev

```

## 6. Proof of work

Save a screenshot of `/docs` or your app as `screenshot.png` in this branch. It shows here:

![Our app](screenshot.png)
