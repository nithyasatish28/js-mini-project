# Team 13 · Lab Equipment Booking

| Team | Partner 1 | Partner 2 | Project | Branch |
|---|---|---|---|---|
| 13 | Monica Irala | Aryan Rao | [Lab Equipment Booking](https://github.com/nithyasatish28/js-mini-project/blob/main/3-lab-equipment-booking.md) | `team-13-lab` |

**Every 3 hours:** update this file, then commit and push it with the message `Check-in Day 1 12:00` (your day and time). Your instructor reads this page on GitHub.

## 1. Who is doing what

Update your own row at every check-in.

| Day | Partner | What will you do? | Completed? | What are you going to work on next? | Stuck on? |
|---|---|---|---|---|---|
| Day 1 | Monica Irala | will do E2,E3,E6 and E7 | ✅ | Frontend components | None |
| Day 1 | Aryan Rao | will do e1,e4,e5 and create database | ✅ | Frontend setup | None |
| Day 2 | Monica Irala | Connect E3, E6, E7 to React (AddEquipment, MyBookings) | ✅ | Demo preparation | None |
| Day 2 | Aryan Rao | Connect E1, E4, E5 to React (EquipmentList, EquipmentItem, booking) | ✅ | Demo preparation | None |
| Day 3 | Monica Irala | Demo & final code review | 🟡 | Explain PRD & components | None |
| Day 3 | Aryan Rao | Demo & final code review | 🟡 | Explain API & database | None |

## 2. Endpoint tracker

Fill in the method and path from your PRD's endpoint table. Status: ✅ done · 🟡 in progress · ⬜ not started

| # | Method + path | Built | Rules checked in /docs | Connected to React | Who |
|---|---|---|---|---|---|
| E1 | `GET /equipment` | ✅ | ✅ | ✅ | Aryan |
| E2 | `GET /equipment/{equipment_id}` | ✅ | ✅ | ✅ | Monica |
| E3 | `POST /equipment` | ✅ | ✅ | ✅ | Monica |
| E4 | `PUT /equipment/{equipment_id}/status` | ✅ | ✅ | ✅ | Aryan |
| E5 | `POST /booking` | ✅ | ✅ | ✅ | Aryan |
| E6 | `GET /bookings/student/{roll_no}` | ✅ | ✅ | ✅ | Monica |
| E7 | `PATCH /booking/{booking_id}/cancel` | ✅ | ✅ | ✅ | Monica |

## 3. Frontend tracker

| Part (from section 5 of your PRD) | Shows the data | Buttons work | Shows API errors | Who |
|---|---|---|---|---|
| Equipment | ✅ | ✅ | ✅ | Aryan |
| My bookings | ✅ | ✅ | ✅ | Monica |
| Add equipment | ✅ | ✅ | ✅ | Monica |

## 4. Blockers and help needed

- None at the moment. All endpoints, frontend components, and rule validations are functioning as specified in the PRD.

## 5. How to run our app

Fill this in by the end of Day 2. Someone who has never seen your code should be able to follow it.

**Backend**

```bash
python -m pip install -r Backend/requirements.txt
python -m uvicorn Backend.main:app --reload --port 8001
```

**Frontend**

```bash
cd Frontend
npm install
npm run dev
```

## 6. Proof of work

Save a screenshot of `/docs` or your app as `screenshot.png` in this branch. It shows here:

![Our app](screenshot.png)
