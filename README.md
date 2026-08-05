# QueryDB
A database for your database queries. Save, tag, and search your SQL snippets instead of losing them in random text files.
# QueryDB

A database for your database queries. Save, tag, and search your SQL snippets instead of losing them in random text files, Slack messages, or Excel Sheets.

## What it does

QueryDB is a full-stack app for storing and organizing SQL queries you write often — reports, one-off debugging queries, recurring analytics pulls, whatever you'd otherwise be copy-pasting from an old file. Tag your queries, search by keyword, and pull them up whenever you need them again.

## Features

- **Auth** — register/login with JWT-based authentication, so your queries are private to you
- **Save queries** — store the query name, the SQL itself, and a report type
- **Tagging** — organize queries with custom tags (many-to-many, so one query can have multiple tags)
- **Search** — find queries by name or SQL content
- **Full CRUD** — create, view, update, and delete both queries and tags

## Tech stack

**Backend**
- FastAPI (Python)
- PostgreSQL
- SQLAlchemy ORM
- Alembic (migrations)
- JWT auth (python-jose) + bcrypt password hashing

**Frontend**
- React (Vite)
- Tailwind CSS
- Shadcn/UI
- React Router

## Running it locally

### Backend
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file:
```
DATABASE_URL=postgresql://postgres:password123@localhost/querydb
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Run migrations and start the server:
```bash
alembic upgrade head
uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## API endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/users/register` | Create a new account |
| POST | `/users/login` | Log in, get a JWT token |
| POST | `/queries` | Create a query |
| GET | `/queries` | List your queries (supports `?search=`) |
| GET | `/queries/{id}` | Get a single query |
| PUT | `/queries/{id}` | Update a query |
| DELETE | `/queries/{id}` | Delete a query |
| POST | `/tags` | Create a tag |
| GET | `/tags` | List your tags (supports `?search=`) |
| DELETE | `/tags/{id}` | Delete a tag |

## Status

Actively in progress — backend is complete, frontend auth flow is done, query management UI is next.

## Why I built this

Built as a portfolio project to go from data analyst to full-stack engineer — first project with a proper many-to-many relationship, PUT endpoints, and a real React frontend on top of a FastAPI backend.
