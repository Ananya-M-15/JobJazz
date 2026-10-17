# JobJazz — Your Career, in Tune 🎵

**JobJazz** is an AI-powered career intelligence platform that helps job seekers understand how well their resumes match job descriptions, identify skill gaps, and build personalized learning roadmaps to improve their career readiness.

🔗 **Live Demo:** [Try JobJazz](https://job-jazz.vercel.app/)

## ✨ Features

- **Resume Analysis:** Extracts relevant information from uploaded PDF resumes.
- **Job Description Matching:** Analyzes resume alignment with job requirements.
- **Skill Gap Analysis:** Identifies missing skills and areas for improvement.
- **AI-Powered Recommendations:** Provides actionable suggestions to strengthen your profile.
- **Personalized Learning Roadmaps:** Organizes skill development into structured learning plans.
- **PDF & OCR Support:** Supports text extraction from PDFs, including scanned documents.
- **Session Recovery:** Helps restore analysis progress after a page refresh.

## 🛠️ Tech Stack

| Category | Technologies |
|---|---|
| Frontend | React, Vite, Tailwind CSS |
| Backend | Python, FastAPI, Pydantic |
| Database | PostgreSQL |
| ORM & Migrations | SQLAlchemy, Alembic |
| AI Integration | Google Gemini API |
| Document Processing | PyMuPDF, Tesseract OCR, Pillow |
| Deployment | Vercel, Render |
| Testing & Quality | Pytest, ESLint |

## 🏗️ Architecture

JobJazz uses a decoupled full-stack architecture:

- **Frontend:** React application deployed on Vercel.
- **Backend:** FastAPI REST API deployed on Render.
- **Database:** PostgreSQL hosted on Neon.
- **AI Layer:** Google Gemini integration with deterministic fallback logic.

## 🚀 Getting Started

### Prerequisites

- Python 3.12
- Node.js and npm
- PostgreSQL
- Google Gemini API key (optional)

### 1. Clone the repository

```bash
git clone https://github.com/Ananya-M-15/JobJazz.git
cd JobJazz
```

### 2. Set up the backend

```bash
python -m venv .venv
```

Activate the virtual environment:

```bash
# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r backend/requirements.txt
```

Configure the required environment variables, including `DATABASE_URL`. Set `GEMINI_API_KEY` if you want to use Gemini-powered features.

Run database migrations and start the backend:

```bash
cd backend
alembic upgrade head
python -m uvicorn app.main:app --reload
```

Backend API documentation: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### 3. Set up the frontend

Open a separate terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the local URL displayed by Vite in your terminal.

## 🧪 Testing

Run the backend test suite from the repository root:

```bash
python -m pytest backend/tests -q
```

Run frontend quality checks:

```bash
cd frontend
npm run lint
npm run build
```

## 🔐 Environment Variables

Configure secrets and environment-specific values through local environment files or your hosting provider's environment settings.

| Variable | Purpose |
|---|---|
| `DATABASE_URL` | PostgreSQL database connection |
| `GEMINI_API_KEY` | Google Gemini API access |
| `CORS_ORIGINS` | Allowed frontend origins |
| `VITE_API_BASE_URL` | Backend API URL used by the frontend |

**Important:** Never commit API keys, database credentials, or other secrets to GitHub.

## 📌 Project Status

JobJazz is deployed and available for exploration. The project combines resume parsing, job matching, skill-gap analysis, and personalized learning recommendations in one application.

## 📄 License

This project is licensed under the MIT License.

---

**Built with Python, React, and AI to help bring your career into tune.**
