# BOOK

BOOK's Online Occupancy Keeper — a workspace/meeting room booking system built for 42 Wolfsburg.

## Overview

BOOK lets 42 students and staff log in with their 42 intra account and reserve meeting rooms for specific time slots. Authentication is handled entirely through 42's OAuth2 flow, with the backend owning the full exchange (authorization, token exchange, session issuance) so that the 42 application secret never reaches the browser.

## Tech Stack

**Backend**
- FastAPI (Python 3.13+)
- PostgreSQL (via `psycopg2-binary`)
- PyJWT for session tokens
- APScheduler for background cleanup jobs
- Loguru for logging
- Managed with `uv` / `pyproject.toml`

**Frontend**
- React (Vite)
- React Router
- Framer Motion
- Tailwind CSS

**Infrastructure**
- Docker Compose (three services: `api`, `frontend`, `postgres`)

## Architecture

```
Browser  <-->  Frontend (Vite, :5173)  <-->  Backend (FastAPI, :9000)  <-->  PostgreSQL (:5432)
                                                    |
                                                    v
                                          42 Intra OAuth2 (api.intra.42.fr)
```

The frontend never talks to 42's API directly. It redirects the browser to the backend's `/auth/login` endpoint, and the backend is responsible for the entire OAuth2 authorization code exchange. This keeps the 42 application secret server-side only, which is required by 42's own OAuth documentation.

## Project Structure

```
.
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes.py          # /auth and /api/rooms routes
│   │   ├── rooms/
│   │   │   ├── service.py         # booking business logic
│   │   │   └── repository.py      # raw SQL / CRUD against Postgres
│   │   ├── database/
│   │   │   └── init.py            # connection pool setup/teardown
│   │   └── models/
│   │       └── schemas.py         # Pydantic request/response models
│   ├── config.py                  # Settings loaded from environment
│   ├── main.py                    # FastAPI app, CORS, lifespan, logging
│   ├── utils/
│   │   └── cleanup.py             # scheduled deletion of past bookings
│   ├── .env.example
│   └── pyproject.toml
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Landing.jsx        # login screen
│   │   │   ├── Header.jsx         # top bar + logout
│   │   │   ├── AuthGate.jsx       # route protection + AuthContext
│   │   │   ├── CalendarView.jsx
│   │   │   ├── CalendarHeader.jsx
│   │   │   ├── BookingModal.jsx
│   │   │   └── ResponsiveLayout.jsx
│   │   ├── hooks/
│   │   │   ├── useCalendar.js
│   │   │   └── useBookings.js
│   │   ├── data/
│   │   │   └── rooms.js           # hardcoded room list
│   │   └── App.jsx
│   ├── index.html
│   └── Dockerfile
└── docker-compose.yml
```

## Prerequisites

- Docker and Docker Compose
- A registered application on 42's intra (https://profile.intra.42.fr/oauth/applications) to obtain a client UID and secret
- Ubuntu/Linux shell

## Environment Variables

Two `.env` files are required, both based on the `.env.example` templates already in the repository.

**`backend/.env`**

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

**`frontend` (via `docker-compose.yml` / Vite)**

| Variable | Purpose |
|---|---|
| `VITE_API_URL` | Base URL the frontend uses to reach the backend API |

These three variables are intentionally kept separate rather than reused, since each serves a different contract: `REDIRECT_URI` is agreed with 42, `VITE_API_URL` is the frontend's own API base, and `FRONTEND_URL` is only the post-login browser destination.

## Running the Project

1. Copy the environment templates and fill in real values:
   ```bash
   cp backend/.env.example backend/.env
   ```
   Then edit `backend/.env` with your database credentials and 42 OAuth application details.

2. Start all services:
   ```bash
   docker compose up --build
   ```

3. Open the app:
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:9000

## Authentication Flow

1. The user clicks "Login with 42" on the frontend, which redirects the browser to `GET /auth/login` on the backend.
2. The backend builds the 42 authorization URL (with a randomly generated `state` value for CSRF protection) and redirects the browser to `api.intra.42.fr`.
3. After the user authorizes the application, 42 redirects back to `GET /auth/callback` with an authorization code.
4. The backend exchanges the code for a 42 access token, fetches the user's profile from `/v2/me`, and issues its own signed JWT.
5. The JWT is set as an `httponly`, `samesite=lax` cookie named `session`, and the browser is redirected to `FRONTEND_URL`.
6. `GET /auth/me` lets the frontend check whether a valid session exists (used by `AuthGate.jsx` to protect routes).
7. `GET /auth/logout` deletes the session cookie server-side; the frontend then navigates to `/login` with `{ replace: true }` to prevent returning to a protected page via the back button.

## API Endpoints

**Auth**
| Method | Path | Description |
|---|---|---|
| GET | `/auth/login` | Redirects to 42's OAuth authorization page |
| GET | `/auth/callback` | Handles the OAuth code exchange and sets the session cookie |
| GET | `/auth/me` | Returns the logged-in user's intra login if the session is valid |
| GET | `/auth/logout` | Clears the session cookie |

**Rooms and Bookings**
| Method | Path | Description |
|---|---|---|
| GET | `/api/rooms` | Lists all bookings (development/testing use) |
| GET | `/api/rooms/{room_name}/bookings` | Lists bookings for a specific room |
| GET | `/api/rooms/{room_name}/bookings/{id}` | Retrieves a single booking |
| POST | `/api/rooms/{room_name}/bookings` | Creates a new booking |
| PATCH | `/api/rooms/{room_name}/bookings/{id}` | Updates an existing booking |
| DELETE | `/api/rooms/{room_name}/bookings/{id}` | Deletes a booking |

## Current Status

The OAuth2 authentication system is functionally complete: login, callback, session validation, and logout are all implemented on the backend, with matching route protection and logout handling on the frontend.

The current focus is connecting the data pipeline between backend and frontend, replacing the hardcoded room and booking data on the frontend (`src/data/rooms.js`) with live calls to the `/api/rooms` endpoints.

## Design Principles

- Minimal dependencies on both backend and frontend; prefer built-in tools (React Context over a state management library, PyJWT over a heavier auth framework) over adding new libraries.
- The backend owns the OAuth2 flow end to end; the frontend only triggers and reacts to it.
- Session state is stored in an `httponly` cookie rather than local storage, to reduce exposure to XSS.
