# Team 06 · Hostel Complaint Tracker

| Team | Partner 1 | Partner 2 | Project | Branch |
|---|---|---|---|---|
| 06 | Darsh Keshav | Rehaan Saha | [Hostel Complaint Tracker](https://github.com/nithyasatish28/js-mini-project/blob/main/1-hostel-complaint-tracker.md) | `team-06-hostel` |

**Every 3 hours:** update this file, then commit and push it with the message `Check-in Day 1 12:00` (your day and time). Your instructor reads this page on GitHub.

## 1. Who is doing what

Update your own row at every check-in.

| Day | Partner | What will you do? | Completed? | What are you going to work on next? | Stuck on? |
|---|---|---|---|---|---|
| Day 1 | Darsh Keshav | Set up Git and the team-06-hostel branch. Create the Vite React app in frontend | YES | Frontend | NTG as off |
| Day 1 | Rehaan Saha | Create hostel.db with the complaints and updates tables and 8 seed complaints | YES | Frontend | NTG as of |
| Day 2 | Darsh Keshav | Connect the React app to the API. Write the fetch functions for E1-E7 in App.jsx. Build the Warden: status counts, complaint cards, status and category filters, and  Show API error messages on the page. | YES | Test the whole app with Rehaan, fill in the README run steps, add the screenshot, and prepare for the demo. | NTG as of now |
| Day 2 | Rehaan Saha | Finish and test all 7 endpoints and the rules in /docs. Build Raise a complaint and My complaints in React. | YES | Test the whole app with Darsh, check the data survives an API restart, fill in the README run steps, add the screenshot, and prepare for the demo. | Ntg as of now |
| Day 3 | Darsh Keshav | Bugs and minor changes. |  |  |  |
| Day 3 | Rehaan Saha | Bugs and minor changes. |  |  |  |

## 2. Endpoint tracker

Fill in the method and path from your PRD's endpoint table. Status: ✅ done · 🟡 in progress · ⬜ not started
| ID | Method and path | API status | Frontend status | Test status | Owner |
|---|---|---|---|---|---|
| E1 | GET /complaints?status=&category= | ✅ | ✅ | ✅ | Rehaan (Functions), Darsh (AP1 & React) |
| E2 | GET /complaints/{id} | ✅ | ✅ | ✅ | Rehaan (Functions), Darsh (AP1 & React) |
| E3 | POST /complaints | ✅ | ✅ | ✅ | Rehaan (Functions), Darsh (AP1 & React) |
| E4 | PATCH /complaints/{id}/status | ✅ | ✅ | ✅ | Rehaan (Functions), Darsh (AP1 & React) |
| E5 | GET /students/{roll_no}/complaints | ✅ | ✅ | ✅ | Rehaan (Functions), Darsh (AP1 & React) |
| E6 | DELETE /complaints/{id} | ✅ | ✅ | ✅ | Rehaan (Functions), Darsh (AP1 & React) |
| E7 | GET /stats | ✅ | ✅ | ✅ | Rehaan (Functions), Darsh (AP1 & React) |

## 3. Frontend tracker

| Part (from section 5 of your PRD) | Shows the data | Buttons work | Shows API errors | Who |
|---|---|---|---|---|
| Warden | ✅ | ✅ | ✅ | Darsh |
| My complaints | ✅ | ✅ | ✅ | Rehaan |
| Raise a complaint | ✅ | ✅ | ✅ | Rehaan |

## 4. Blockers and help needed

- 

## 5. How to run our app

Fill this in by the end of Day 2. Someone who has never seen your code should be able to follow it.

**Backend**

```bash
cd backend

```

**Frontend**

```bash
cd frontend

```

## 6. Proof of work

Save a screenshot of `/docs` or your app as `screenshot.png` in this branch. It shows here:

![Our app](screenshot.png)
