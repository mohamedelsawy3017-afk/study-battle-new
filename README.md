# ⚔️ Study Battle

> A gamified study competition app. Who's locking in today? 💀

Two users compete to see who studies more. It's a todo app but with leaderboards,
progress bars, levels, badges, and trash talk. Because studying alone is boring.

---

## 🚀 Quick Start

### Backend (FastAPI + SQLite)

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

The backend will:
- Auto-create the SQLite database on first run
- Serve both the API and the frontend static files
- Be available at http://localhost:8000

### Frontend

Static HTML/CSS/JS files in `frontend/`. Served automatically by FastAPI.
Open http://localhost:8000 in your browser.

---

## 📁 Project Structure

```
study_battle/
├── backend/
│   ├── main.py              # FastAPI app entry point
│   ├── core/
│   │   ├── config.py        # Settings (SECRET_KEY, DB URL, etc.)
│   │   ├── security.py      # JWT + bcrypt password hashing
│   │   └── dependencies.py  # get_current_user dependency
│   ├── database/
│   │   └── session.py       # Async SQLAlchemy engine + session
│   ├── models/
│   │   ├── user.py          # User model + level/badge logic
│   │   └── task.py          # Task model
│   ├── schemas/
│   │   ├── auth.py          # Register/Login/Token schemas
│   │   ├── user.py          # UserPublic, UserStats, Leaderboard
│   │   └── task.py          # TaskCreate, TaskUpdate, TaskResponse
│   ├── services/
│   │   ├── user_service.py  # User CRUD + score/level update
│   │   └── task_service.py  # Task CRUD + complete (awards score)
│   └── routers/
│       ├── auth.py          # POST /auth/register, /auth/login
│       ├── users.py         # GET /users/me, /leaderboard, /{username}
│       └── tasks.py         # CRUD /tasks/ + POST /tasks/{id}/complete
└── frontend/
    ├── index.html           # Entry point (auto-redirects)
    ├── login.html           # Login + Register page
    ├── dashboard.html       # Main app (tasks, leaderboard, compare)
    └── api.js               # Centralized fetch-based API client
```

---

## 🔌 API Endpoints

### Auth
| Method | Path | Description |
|--------|------|-------------|
| POST | /api/auth/register | Create account, returns JWT |
| POST | /api/auth/login | Login, returns JWT |

### Users (🔒 requires Bearer token)
| Method | Path | Description |
|--------|------|-------------|
| GET | /api/users/me | Current user profile |
| GET | /api/users/me/stats | Full stats with task counts |
| GET | /api/users/leaderboard | Top users by score |
| GET | /api/users/{username} | Another user's profile |
| GET | /api/users/{username}/stats | Another user's stats (for compare) |

### Tasks (🔒 requires Bearer token)
| Method | Path | Description |
|--------|------|-------------|
| GET | /api/tasks/ | List all my tasks |
| POST | /api/tasks/ | Create a task |
| PATCH | /api/tasks/{id} | Update a task |
| POST | /api/tasks/{id}/complete | Mark done → awards score |
| DELETE | /api/tasks/{id} | Delete a task |

---

## 🎮 Game Mechanics

| Study Score | Level | Badge |
|------------|-------|-------|
| 0 min | 1 | Rookie 🐣 |
| 30 min | 2 | Warming Up 🔥 |
| 120 min | 3 | Focused 🎯 |
| 300 min | 4 | Grinder 💪 |
| 600 min | 5 | Scholar 📚 |
| 1200 min | 6 | Beast Mode 🦁 |
| 2400 min | 7 | Legend 👑 |

Completing a task awards its estimated minutes to your study score.

---

## 🗄 Switching to PostgreSQL

In `backend/core/config.py`, change:
```python
DATABASE_URL: str = "postgresql+asyncpg://user:pass@localhost/study_battle"
```
And install: `pip install asyncpg`

---

## 🔐 Production Notes

- Change `SECRET_KEY` in `core/config.py` (or set via `.env`)
- Set `DEBUG = False`
- Restrict CORS origins in `main.py`
- Use a proper PostgreSQL database
- Put behind nginx + HTTPS
