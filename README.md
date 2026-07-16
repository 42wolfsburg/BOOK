# BOOK

BOOK's Online Occupancy Keeper — a workspace/meeting room booking system built for 42 Wolfsburg.

## Overview

BOOK lets 42 students and staff log in with their 42 intra account and reserve meeting rooms for specific time slots. Authentication is handled entirely through 42's OAuth2 flow, with the backend owning the full exchange (authorization, token exchange, session issuance) so that the 42 application secret never reaches the browser. Bookings for four staff-managed rooms also sync with Google Calendar, so the rooms' real calendars — the ones the org already sees by default — stay up to date automatically.

## Tech Stack

**Backend**
- FastAPI (Python 3.13+)
- PostgreSQL (via `psycopg2-binary`)
- PyJWT for session tokens
- APScheduler for background cleanup jobs
- Loguru for logging
- `httpx` for all outbound HTTP (42 OAuth, Google Apps Script)
- Managed with `uv` / `pyproject.toml`

**Frontend**
- React (Vite)
- React Router
- Framer Motion
- Tailwind CSS
- `react-big-calendar` + `moment`

**Google Calendar integration**
- Google Apps Script (one deployment per room, running as that room's own Google account)
- No service accounts, no OAuth libraries, no Google API client libraries — plain `httpx` calls to each script's Web App URL, and a webhook endpoint that receives pushes back

**Infrastructure**
- Docker Compose (three services: `api`, `frontend`, `postgres`)
- Two-layer nginx reverse proxy in production (outer SSL termination → inner Docker host)

## Architecture

```
Browser  <-->  Frontend (Vite, :5173)  <-->  Backend (FastAPI, :9000)  <-->  PostgreSQL (:5432)
                                                    |
                                                    |--> 42 Intra OAuth2 (api.intra.42.fr)
                                                    |
                                                    '--> Google Apps Script (per room)  <-->  Google Calendar
                                                             ^                                (dummy account +
                                                             |________________________________ resource calendar)
                                                          /api/google/webhook
```

The frontend never talks to 42's API or Google's API directly. It redirects the browser to the backend's `/auth/login` endpoint for 42 authentication, and never touches Google at all — Google Calendar sync is an invisible side effect of booking, update, and delete operations, entirely server-to-server.

## Project Structure

```
.
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes.py            # /api/rooms routes
│   │   ├── auth/
│   │   │   └── routes.py            # /auth routes (42 OAuth2)
│   │   ├── rooms/
│   │   │   ├── service.py           # booking business logic, calls into google/service.py
│   │   │   └── repository.py        # raw SQL / CRUD against Postgres
│   │   ├── google/
│   │   │   ├── service.py           # outbound calls to each room's Apps Script Web App
│   │   │   └── routes.py            # /api/google/webhook — inbound pushes from Apps Script
│   │   ├── database/
│   │   │   └── init.py              # connection pool setup/teardown
│   │   └── models/
│   │       └── schemas.py           # Pydantic request/response models
│   ├── config.py                    # Settings loaded from environment
│   ├── main.py                      # FastAPI app, CORS, lifespan, logging, scheduler
│   ├── utils/
│   │   └── cleanup.py               # scheduled deletion of past bookings
│   ├── .env.example
│   └── pyproject.toml
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Landing.jsx          # login screen
│   │   │   ├── Header.jsx           # top bar + logout
│   │   │   ├── AuthGate.jsx         # route protection + AuthContext
│   │   │   ├── CalendarView.jsx
│   │   │   ├── CalendarHeader.jsx
│   │   │   ├── RoomDropdown.jsx
│   │   │   ├── BookingModal.jsx
│   │   │   ├── DeleteBookingModal.jsx
│   │   │   └── ResponsiveLayout.jsx
│   │   ├── hooks/
│   │   │   ├── useCalendar.js
│   │   │   └── useBookings.js
│   │   ├── data/
│   │   │   └── rooms.js             # hardcoded room list
│   │   └── App.jsx
│   ├── index.html
│   └── Dockerfile
├── google-apps-script/
│   └── Code.gs                      # reference copy only — not executed by the app,
│                                     # see "Google Calendar Integration" below
└── docker-compose.yml
```

## Prerequisites

- Docker and Docker Compose
- A registered application on 42's intra (https://profile.intra.42.fr/oauth/applications) to obtain a client UID and secret
- Four Google Workspace accounts acting as room "owners" (the dummy accounts), each with a deployed Apps Script — see below
- Ubuntu/Linux shell

## Environment Variables

Copy `backend/.env.example` to `backend/.env` and fill in real values.

| Variable | Purpose |
|---|---|
| `POSTGRES_USER` | Database username |
| `POSTGRES_PASSWORD` | Database password |
| `POSTGRES_DB` | Database name |
| `POSTGRES_HOST` | Database host (service name in Docker, e.g. `postgres`) |
| `POSTGRES_PORT` | Database port |
| `DATABASE_URL` | Full Postgres connection string |
| `BACKEND_PORT` | Port the FastAPI app listens on (9000) |
| `BACKEND_HOST` | Host the FastAPI app binds to |
| `CLIENT_ID` | 42 application UID |
| `SECRET` | 42 application secret (server-side only, never exposed to the frontend) |
| `REDIRECT_URI` | Callback URL registered with 42, must match `/auth/callback` on the backend exactly |
| `JWT_SECRET` | Long random string used to sign session cookies |
| `FRONTEND_URL` | Where the browser is redirected after a successful login |
| `VITE_API_URL` | Base URL the frontend uses to reach the backend API |
| `GOOGLE_WEBAPP_URL_PISCINE` | Apps Script Web App `/exec` URL for the Piscine room |
| `GOOGLE_WEBAPP_URL_GALAXY` | Apps Script Web App `/exec` URL for the Galaxy room |
| `GOOGLE_WEBAPP_URL_SPACE_INVADER` | Apps Script Web App `/exec` URL for the Space Invaders room |
| `GOOGLE_WEBAPP_URL_GALLERY` | Apps Script Web App `/exec` URL for the Gallery room |
| `GOOGLE_WEBHOOK_SECRET` | Shared secret, identical across all four scripts and the backend, used to authenticate calls in both directions |

## Running the Project

1. Copy the environment template and fill in real values:
   ```bash
   cp backend/.env.example backend/.env
   ```

2. Start all services:
   ```bash
   docker compose up --build
   ```

3. Open the app:
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:9000

Editing `.env` requires a manual restart (`docker compose restart api`) — unlike code changes, environment variable edits are not picked up by `--reload`.

## Authentication Flow

1. The user clicks "Login with 42" on the frontend, which redirects the browser to `GET /auth/login` on the backend.
2. The backend builds the 42 authorization URL (with a randomly generated `state` value for CSRF protection) and redirects the browser to `api.intra.42.fr`.
3. After the user authorizes the application, 42 redirects back to `GET /auth/callback` with an authorization code.
4. The backend exchanges the code for a 42 access token, fetches the user's profile from `/v2/me`, and issues its own signed JWT. `intra` and `is_staff` are always sourced from this trusted JWT via the `get_current_user` dependency, never from client-supplied fields.
5. The JWT is set as an `httponly`, `samesite=lax` cookie named `session`, and the browser is redirected to `FRONTEND_URL`.
6. `GET /auth/me` lets the frontend check whether a valid session exists (used by `AuthGate.jsx` to protect routes).
7. `GET /auth/logout` deletes the session cookie server-side.

## Google Calendar Integration

### Why Apps Script instead of a service account

The original design used four Google Cloud service accounts (one per room) authenticating via signed JWTs. That approach hit a hard wall: Google Workspace **resource calendars** (the room calendars everyone in the org already sees by default) don't expose ACL sharing to external identities like service accounts — not through the UI, and not through the Calendar API's ACL endpoint either. Service accounts were also explicitly blocked from inviting attendees without **Domain-Wide Delegation**, which was ruled out as too broad a grant (it lets a service account impersonate *any* user in the domain for its authorized scope, not just one room's dummy account).

The adopted solution instead uses **Google Apps Script**, deployed once per room while logged into that room's own dummy Google account (e.g. `meeting-piscine@42wolfsburg.de`). A script inherits the real permissions of whoever deployed it — a genuine Workspace user, not an external identity — so it can freely create events, invite the room's resource calendar as an attendee (which auto-accepts), and read anything that account already has default visibility into. No credentials, private keys, or token exchange live in the backend at all.

### How it works

**Outbound (backend → Google), `backend/app/google/service.py`:**
`register_booking`, `update_booking`, and `delete_booking` in `rooms/service.py` each call into `create_event` / `update_event` / `delete_event`, which POST a small JSON payload (action, times, shared secret) to that room's Apps Script Web App URL via `httpx`. The script creates/updates/deletes the event on the dummy account's calendar and invites the room's resource calendar as an attendee. The returned Google event ID is stored on `bookings.google_event_id`, which is what lets later updates/deletes target the correct event.

**Inbound (Google → backend), `backend/app/google/routes.py`:**
Each script has an installable trigger (`onEventUpdated`) watching its resource calendar directly. When something changes — created, rescheduled, or cancelled, whether through the app or by someone editing Google Calendar directly — the trigger fires inside Google's infrastructure and POSTs to `/api/google/webhook` with the change. The backend reconciles it into Postgres via `db_upsert_google_booking` (matches on `google_event_id`; updates an existing row or inserts a new one for events created directly on Calendar) or `db_delete_booking_by_google_event_id` for cancellations. Because the database is kept current via this push, `get_booking_per_room` simply reads Postgres — there is no live Google fetch on the read path.

**Google Meet:** the `create` action uses the Calendar Advanced Service (`Calendar.Events.insert` with `conferenceData`) rather than the simpler `CalendarApp`, so every booking gets a Meet link automatically, created under the room's own dummy account.

### Contributors

[![](https://github.com/fjjdessoycaraballo.png?size=50)](https://github.com/fjjdessoycaraballo)
[![](https://github.com/MikMey.png?size=50)](https://github.com/MikMey)
[![](https://github.com/StefanPenev?size=50)](https://github.com/StefanPenev)

- [spenev](https://github.com/StefanPenev)
- [mimeyer](https://github.com/MikMey)
- [fdessoy-](https://github.com/fjjdessoycaraballo)
