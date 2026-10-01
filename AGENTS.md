==================================================
JOBJAZZ — PERMANENT ENGINEERING RULES
==================================================

PROJECT
-------

Project name:
JobJazz

Tagline:
"Your career, in tune."

Root:
D:\Project\JobJazz

JobJazz is a full-stack AI-powered career analysis platform.

The core product goal is:

A user uploads their resume, provides a job description,
and JobJazz analyzes the fit, identifies skill gaps,
provides actionable recommendations, and eventually
helps the user discover relevant job opportunities
and companies.

==================================================
1. GENERAL DEVELOPMENT PRINCIPLES
==================================================

1. Inspect before modifying.

Before changing code, inspect the relevant existing files,
interfaces, models, routes, tests, and dependencies.

Never assume a file, function, schema, API response,
or service exists without checking.

2. Preserve working functionality.

Do not rewrite working systems unnecessarily.

Prefer minimal, targeted modifications.

3. Reuse existing infrastructure.

If a service already performs a required operation,
reuse it rather than creating a duplicate implementation.

4. Do not perform unrelated refactors.

A phase should modify only what is necessary for that phase.

5. Do not redesign existing UI unless explicitly requested.

Preserve the established JobJazz visual identity.

6. Do not introduce unnecessary dependencies.

Before adding a package, determine whether the existing
stack can solve the problem.

7. Do not expose secrets.

Never print, commit, or hardcode:

.env
GEMINI_API_KEY
DATABASE_URL
credentials
tokens
API keys

8. Do not claim completion without testing.

Implementation is not complete until relevant tests,
linting, builds, and endpoint checks have been performed.

==================================================
2. EXISTING TECHNOLOGY STACK
==================================================

Backend:

Python
FastAPI
Pydantic
SQLAlchemy
PostgreSQL
Alembic
PyMuPDF
Pillow
pytesseract
Google Gemini API

Frontend:

React
Vite
Tailwind CSS
Lucide React
Motion

Database:

PostgreSQL running through Docker during development.

Development database:

jobjazz

Backend development command:

python -m uvicorn app.main:app --reload

Do not replace this with direct uvicorn.exe execution
because the Windows environment may block the executable.

Frontend:

npm run dev

==================================================
3. CURRENT PROJECT ARCHITECTURE
==================================================

Major directories:

backend/
frontend/
data/
models/
tests/

Backend application:

backend/app/

Frontend:

frontend/src/

Frontend API wrapper:

frontend/src/api/jobjazzApi.js

Frontend components:

frontend/src/components/

==================================================
4. EXISTING CORE PIPELINE
==================================================

The backend already contains these capabilities:

Resume:

PDF
 ↓
PDF/document extraction
 ↓
OCR fallback where required
 ↓
text cleaning
 ↓
resume NLP/profile extraction
 ↓
ResumeProfile

Job Description:

JD text
 ↓
JD parser
 ↓
JobProfile

Matching:

ResumeProfile
+
JobProfile
 ↓
matching engine
 ↓
MatchResult

Skill Gap:

MatchResult
 ↓
SkillGapResult

Recommendations:

MatchResult
+
SkillGapResult
 ↓
AI recommendation engine
or deterministic fallback
 ↓
RecommendationResult

Database:

User
Resume
JobDescription
Analysis
SkillGap
Recommendation

Do not recreate these systems unless inspection proves
that a necessary change is required.

==================================================
5. EXISTING API CONTRACTS
==================================================

Existing routes include:

POST /resume/extract

POST /job-description/analyze

POST /matching/analyze

POST /skill-gap/analyze

POST /recommendations/generate

Preserve these routes unless a phase explicitly requires
a compatible extension.

Do not silently rename or remove routes.

==================================================
6. FRONTEND PRODUCT FLOW
==================================================

Current product flow:

Landing Page
 ↓
Get Started
 ↓
Resume Upload
 ↓
Career Profile
 ↓
Job Description Input
 ↓
Matching
 ↓
Skill Gaps
 ↓
Recommendations
 ↓
Final JobJazz Report

Future:

Final Report
 ↓
Relevant Opportunities
 ↓
Relevant Roles
 ↓
Relevant Companies
 ↓
Job Market Analytics

The final product should answer:

"What opportunities fit me,
how well do I match them,
what am I missing,
and what should I do next?"

==================================================
7. UI RULES
==================================================

Existing visual direction:

Dark
Purple
Glassmorphism
Subtle borders
Soft gradients
Modern typography
Minimal but polished

Existing Background and Navbar are established.

Do not redesign them unless explicitly requested.

Do not replace the existing design with generic dashboards.

Avoid excessive cards and unnecessary information.

Prefer progressive disclosure.

Show users insights rather than internal implementation details.

Do not expose:

database UUIDs
raw API responses
raw JSON
internal parser metadata
debug information

unless explicitly requested for development/debugging.

==================================================
8. PRODUCT UX PRINCIPLE
==================================================

The user does NOT primarily want to see:

"Here is what we extracted from your resume."

The user wants:

"Here is what your resume means for your career."

Therefore:

Internal data:
ResumeProfile
JobProfile
MatchResult
SkillGapResult
RecommendationResult

should be transformed into understandable user-facing insights.

Example:

Instead of exposing:

resume_id:
52fde4c7...

show:

Resume analyzed successfully.

Instead of dumping:

required_skills:
[...]

show:

Required skills you match
and
Required skills you're missing.

==================================================
9. PDF HANDLING
==================================================

When a PDF must be processed:

First inspect existing PDF/document extraction services.

Reuse existing extraction and OCR infrastructure.

Do not create duplicate PDF extraction pipelines.

Resume PDFs and Job Description PDFs should use
consistent extraction infrastructure where practical.

==================================================
10. BACKEND RULES
==================================================

Use FastAPI dependency injection for database sessions.

Use SQLAlchemy models for persistence.

Use Pydantic models for API contracts.

Validate external input.

Return clear HTTP errors.

Do not expose stack traces to clients.

Keep business logic in services rather than putting
large amounts of logic directly inside route handlers.

==================================================
11. DATABASE RULES
==================================================

Do not change the schema unnecessarily.

If schema changes are required:

1. Modify SQLAlchemy model.
2. Create Alembic migration.
3. Apply migration.
4. Run database tests.

Never manually modify production-like database state
without a migration.

==================================================
12. TESTING RULES
==================================================

After backend changes:

pytest

After frontend changes:

npm run lint
npm run build

For new API routes:

Test the route directly.

For new frontend flows:

Test the complete user interaction.

Never delete tests simply to make the suite pass.

==================================================
13. TESTING PRIORITY
==================================================

Prefer:

unit tests
integration tests
API tests
database tests
manual Swagger verification
frontend build/lint

Existing passing tests must continue passing.

==================================================
14. AI/GEMINI RULES
==================================================

Do not hardcode API keys.

Use the existing Gemini service.

Prefer structured Pydantic output when using Gemini.

AI output must be constrained by the structured
information available to JobJazz.

Do not allow AI to invent resume skills,
experience, education, certifications,
or job requirements.

Deterministic fallback behavior should remain available
where already implemented.

==================================================
15. DEVELOPMENT WORKFLOW
==================================================

For every task:

1. Inspect.
2. Plan.
3. Modify.
4. Test.
5. Fix.
6. Retest.
7. Report.

Do not stop immediately after writing code.

==================================================
16. PHASE BOUNDARIES
==================================================

Work only on the requested phase.

Do not implement future phases unless explicitly requested.

Do not modify unrelated files.

At the end of a phase, report:

- files inspected
- files created
- files modified
- tests run
- test results
- build results
- remaining issues
- recommended next phase

==================================================
17. GIT SAFETY
==================================================

Do not commit unless explicitly requested.

Before suggesting a commit:

check:

git status
git diff

Never commit:

.env
secrets
credentials
large generated files
node_modules
Python virtual environments

==================================================
18. CURRENT PRIORITY
==================================================

The immediate priority is to finish a working,
demonstrable JobJazz MVP.

Prioritize:

1. Complete end-to-end resume → JD → match pipeline.
2. Skill gaps.
3. Recommendations.
4. Polished analysis dashboard.
5. Job/company opportunity discovery.
6. Testing.
7. Deployment/demo readiness.
8. Documentation.

Avoid spending excessive time on low-value polish
before the core user journey works.

==================================================
19. COMMUNICATION
==================================================

When implementing a task:

Do not ask for clarification if the answer can be
determined by inspecting the repository.

If a genuine ambiguity exists, explain it clearly.

Never claim that something works unless it was tested.

Be explicit about failures.

==================================================
20. MOST IMPORTANT RULE
==================================================

JobJazz should be treated as a real product, not merely
a collection of API endpoints.

Every implementation should preserve this goal:

"Your career, in tune."

Build the underlying engineering correctly,
but always connect technical implementation
to a useful user-facing career insight.

==================================================

End of JobJazz permanent engineering rules.
