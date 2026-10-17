# JobJazz — Your Career, in Tune.

JobJazz is a full-stack, AI-powered career intelligence and resume optimization platform. It bridges the gap between candidate resumes and job descriptions by analyzing skill alignments, identifying critical experience/education gaps, generating prioritized action plans, and building tailored, week-by-week learning roadmaps.

---

## Architecture & Technology Stack

```
   ┌──────────────────────────────────────────────────────────────┐
   │                 Frontend (React 18 + Vite)                  │
   │  - Tailwind CSS + Glassmorphism UI                          │
   │  - Interactive Dashboard, Skills Matrix, Learning Roadmap   │
   │  - Session Recovery & Client-side Preference Management     │
   └──────────────────────────────┬───────────────────────────────┘
                                  │ HTTP / JSON REST APIs
                                  ▼
   ┌──────────────────────────────────────────────────────────────┐
   │                 Backend (FastAPI + Python 3.12)              │
   │  - PyMuPDF + Tesseract OCR Document Extraction Engine        │
   │  - Deterministic Profile Extraction & Skill Gap Engine       │
   │  - Google Gemini AI Integration (with Deterministic Fallback)│
   │  - Pydantic v2 Schema Validation & Timetable Scheduler       │
   └──────────────────────────────┬───────────────────────────────┘
                                  │ SQLAlchemy 2.0 / Alembic
                                  ▼
   ┌──────────────────────────────────────────────────────────────┐
   │                 Database (PostgreSQL 17)                     │
   │  - Users, Resumes, Job Descriptions, Match Analyses,         │
   │    Skill Gaps, Recommendations, and Learning Roadmaps        │
   └──────────────────────────────────────────────────────────────┘
```

- **Frontend**: React 18, Vite, Tailwind CSS, Lucide React, Motion.
- **Backend**: Python 3.12, FastAPI, Pydantic v2, SQLAlchemy 2.0, Alembic, PyMuPDF (`fitz`), Pillow, PyTesseract.
- **Database**: PostgreSQL (Docker for local development; managed PostgreSQL in production).
- **AI Engine**: Google Gemini API (`gemini-2.5-flash` / `gemini-1.5-flash`) with robust deterministic fallback.

---

## Local Development Quickstart

### 1. Prerequisites
- **Python**: 3.11 or 3.12
- **Node.js**: 18.x or 20.x with `npm`
- **Docker**: For local PostgreSQL container

### 2. Start PostgreSQL
```bash
docker compose up -d db
```
The database runs on `localhost:5432` with credentials `postgres:postgres` and database `jobjazz`.

### 3. Backend Setup
From the repository root:
```bash
# Create and activate virtual environment
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt

# Configure environment
cp .env.example .env
# Edit .env to set GEMINI_API_KEY if testing AI capabilities

# Apply database migrations
cd backend
alembic upgrade head
cd ..

# Run development server
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
Backend API interactive docs: `http://127.0.0.1:8000/docs`
Health check: `http://127.0.0.1:8000/health`

### 4. Frontend Setup
In a separate terminal:
```bash
cd frontend

# Install dependencies
npm install

# Start Vite dev server
npm run dev
```
Frontend application: `http://localhost:5173`

---

## Testing & Quality Assurance

### Run Backend Test Suite
```bash
# From repository root
pytest backend/tests
```

### Run Frontend Linting & Production Build
```bash
cd frontend
npm run lint
npm run build
```

---

## Environment Variables Reference

### Backend (`.env` or Cloud Service Settings)
| Variable | Required | Default | Description |
|---|---|---|---|
| `DATABASE_URL` | Yes | `postgresql://postgres:postgres@localhost:5432/jobjazz` | PostgreSQL connection string. Supports `postgres://` or `postgresql://`. |
| `GEMINI_API_KEY` | No | None | Google Gemini API key. If omitted, JobJazz operates seamlessly using deterministic engines. |
| `CORS_ORIGINS` | No | `http://localhost:5173,http://127.0.0.1:5173,http://localhost:4173` | Comma-separated list of allowed web client origins. |
| `ENVIRONMENT` | No | `development` | Deployment environment name (`development`, `production`). |

### Frontend (`frontend/.env` or Build Settings)
| Variable | Required | Default | Description |
|---|---|---|---|
| `VITE_API_URL` | No | `http://127.0.0.1:8000` | Backend API base URL accessible from the user's browser. |

---

## Recommended Production Deployment Architecture

JobJazz is architected as a decoupled SPA frontend, FastAPI backend, and PostgreSQL database.

```
+-------------------------------------------------------+
|  Frontend: Vercel / Netlify / Cloudflare Pages        |
|  - Continuous deployment from Git                     |
|  - Build Command: npm run build                       |
|  - Output Directory: dist                             |
|  - Environment Variable: VITE_API_URL                 |
+---------------------------+---------------------------+
                            | HTTPS
                            v
+-------------------------------------------------------+
|  Backend: Render / Railway / Fly.io / AWS App Runner  |
|  - Python 3.12 Web Service or Docker container        |
|  - Health Check Path: /health                         |
|  - Startup: uvicorn app.main:app --host 0.0.0.0       |
|  - Environment: DATABASE_URL, GEMINI_API_KEY,         |
|                 CORS_ORIGINS                          |
+---------------------------+---------------------------+
                            | Managed Connection
                            v
+-------------------------------------------------------+
|  Database: Managed PostgreSQL (Neon, Supabase, Render)|
|  - Highly available PostgreSQL 15+                    |
|  - Run: alembic upgrade head during release phase     |
+-------------------------------------------------------+
```

### Production Deployment Steps

1. **Database Setup (e.g., Neon / Supabase / Render PostgreSQL)**:
   - Create a PostgreSQL database instance.
   - Note the connection string (e.g. `postgresql://user:pass@host/dbname?sslmode=require`).

2. **Backend Setup (e.g., Render Web Service)**:
   - Connect the repository with root set to `backend` or use the root `Dockerfile` / `backend/Dockerfile`.
   - Build command: `pip install -r requirements.txt`
   - Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - Set Environment Variables:
     - `DATABASE_URL`: Your managed PostgreSQL URL.
     - `CORS_ORIGINS`: Your frontend URL (e.g., `https://jobjazz.vercel.app`).
     - `GEMINI_API_KEY`: Your Gemini API key.
   - Run initial migrations: execute `alembic upgrade head` via release command or SSH console.

3. **Frontend Setup (e.g., Vercel / Netlify)**:
   - Connect repository with root set to `frontend`.
   - Framework preset: Vite.
   - Set Environment Variable:
     - `VITE_API_URL`: Your deployed backend URL (e.g., `https://api.jobjazz.com`).
   - Trigger deployment.

---

## Production Considerations & Caveats

1. **Free-Tier Cold Starts**:
   - If using free-tier providers (such as Render or Railway free hobby instances), instances spin down after inactivity. The first API request may take 30–50 seconds while the container initializes.
2. **File Upload Limits & OCR**:
   - Resumes and Job Description uploads are validated strictly for file signatures (`%PDF`, PNG, JPEG) and enforced to a **5 MB** ceiling with HTTP 413 Payload Too Large error handling.
   - Document text extraction uses PyMuPDF first, falling back to Tesseract OCR for scanned pages.
3. **Session Recovery**:
   - Analysis results and roadmap state are referenced by an anonymous, non-sensitive UUID stored in `sessionStorage`. Browser refreshes recover dashboard state without persisting personal resume text in browser storage.
4. **Deterministic Fallbacks**:
   - If Gemini API quota limits are exceeded or the API key is not supplied, the platform falls back to deterministic recommendations and catalog-vetted learning resources without interruption.

---

## License

MIT License. Designed and developed for JobJazz.
