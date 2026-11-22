
# JonoSeba (জনসেবা)

**AI-powered Municipal Citizen Service Assistant**

JonoSeba is a Bangladesh-focused educational project built
with FastAPI, PostgreSQL, React, Gemini, RAG, and MCP.

It helps citizens submit municipal complaints, track their
current status, and ask questions about citizen services.

**Disclaimer:** JonoSeba is an independent educational
demo, not an official government-operated portal.

## 1. Problem and target users

Citizens often need to find service information from
multiple sources and follow up on complaints manually.

JonoSeba provides one interface for:
- Municipal service guidance
- Citizen complaint submission
- Complaint status tracking
- Administrative complaint management
- AI-assisted questions in Bangla and English

Target users are citizens and small municipal service
teams in Bangladesh.

## 2. Main features

### Citizen
- Register and log in with email and password
- Submit complaints to active departments
- View personal complaint records
- Track current complaint status
- Use the AI chat assistant

### Administrator
- Log in using an authorized admin account
- View complaints from all citizens
- Search and filter complaints
- Update complaint status
- View complaint statistics

### AI backend
- Gemini language model integration
- Multi-turn chat request support
- Database-backed tool calling
- pgvector-based knowledge retrieval components
- MCP integration modules

AI tool execution, published knowledge coverage, and
MCP transport behavior must be verified with live tests
before the final demonstration.

## 3. Technology stack

| Layer | Technology |
|---|---|
| Backend | Python, FastAPI |
| Database | PostgreSQL, pgvector |
| ORM | Async SQLAlchemy |
| Migrations | Alembic |
| Authentication | JWT, Argon2 |
| AI | Gemini |
| RAG | Embeddings and PostgreSQL vector search |
| MCP | Python MCP integration |
| Frontend | React, TypeScript, Vite |
| Development tooling | uv, pytest |
| Containerization | Docker Compose |

## 4. Local backend setup

Requirements:
- Python 3.12
- uv
- PostgreSQL with pgvector
- Required API credentials

Clone the repository, then from the project root:

    uv sync --frozen
    cp .env.example .env

Edit `.env` and provide the required values described
in `.env.example`.

Never commit `.env` or real API credentials.

Create the PostgreSQL database and enable pgvector:

    CREATE EXTENSION IF NOT EXISTS vector;

Run database migrations:

    uv run alembic upgrade head

Seed municipal departments:

    uv run python -m scripts.seed_departments

Start the backend:

    uv run uvicorn app.main:app --reload --port 8000

Open:

    http://127.0.0.1:8000/docs

## 5. Docker setup

Docker Compose provides an isolated backend and
PostgreSQL/pgvector environment.

Create the real `.env` file from `.env.example`.
Provide all application secrets and API credentials.

Create a separate, Git-ignored `.env.docker` file:

    POSTGRES_PASSWORD=YOUR_LONG_RANDOM_ALPHANUMERIC_PASSWORD

Start:

    docker compose --env-file .env.docker up --build -d

Check logs:

    docker compose --env-file .env.docker logs api --tail=100

Open Swagger:

    http://127.0.0.1:8000/docs

Seed departments inside the running container:

    docker compose --env-file .env.docker exec api uv run --no-sync python -m scripts.seed_departments

Stop containers:

    docker compose --env-file .env.docker down

Do not use `down -v` unless you intentionally want to
delete the isolated Docker database volume.

The Docker startup process runs Alembic migrations.

The external Gemini embedding dependency and the
complete embedding-service deployment requirement
will be verified separately before final submission.

## 6. Frontend setup

From the repository root:

    cd frontend
    npm install
    npm run dev

Default development URL:

    http://localhost:5173

Production build:

    npm run build

## 7. Main API endpoints

All primary application APIs use `/api/v1`.

| Method | Endpoint | Purpose |
|---|---|---|
| POST | /api/v1/auth/register | Register a citizen |
| POST | /api/v1/auth/login | Obtain a JWT |
| GET | /api/v1/auth/me | Read current user |
| GET | /api/v1/departments | List departments |
| POST | /api/v1/complaints | Submit complaint |
| GET | /api/v1/complaints | List allowed complaints |
| GET | /api/v1/complaints/{id} | Read one complaint |
| PATCH | /api/v1/complaints/{id} | Update a complaint |
| DELETE | /api/v1/complaints/{id} | Delete a complaint |
| POST | /api/v1/chat | Send a chat request |

Swagger shows the exact request/response schemas
and authentication requirements.

### Example complaint request

    {
      "title": "Broken streetlight",
      "description": "The streetlight has not worked for several days.",
      "location": "Savar, Dhaka",
      "department_id": 1
    }

`department_id` must refer to a real active department.

### Example chat request

    {
      "message": "How can I apply for a trade license?",
      "history": []
    }

The assistant must not invent official fees, document
requirements, timelines, or government approval.

## 8. Architecture and data flows

### Domain API

Client → FastAPI controller → dependency injection →
service → repository → PostgreSQL → Pydantic response

### Authentication

Registration → Argon2 password hash → database

Login → password verification → expiring JWT

Protected request → token validation → current user
and database role → authorization

### AI and tools

Chat endpoint → service → Gemini integration →
model tool selection → database-backed tool →
tool result → model answer

### RAG

Source documents → review/ingestion → chunks →
embeddings → pgvector

Question → query embedding → vector retrieval →
grounded AI answer or insufficient-evidence response

### MCP

MCP client → HTTP or stdio transport →
MCP tool/resource/prompt → application services

Both transports must be demonstrated against the
running backend.

## 9. Testing

Backend:

    uv run pytest -q

Frontend:

    cd frontend
    npm run build

Manual acceptance tests:
- Register and log in
- Citizen creates a complaint
- Admin reviews and changes its status
- Citizen sees the updated status
- Gemini answers a basic question
- A database-backed AI tool is used
- A RAG answer uses published source evidence
- MCP tools work over HTTP and stdio

## 10. Knowledge base

The knowledge system is intended to support:
- Birth registration
- Death registration
- Trade licenses
- Holding tax
- Municipal complaint guidance

Publication must use reviewed, source-linked information.

The knowledge ingestion/publication entrypoint and
successful retrieval of published chunks still need
final verification.

## 11. Business model

**Potential customers:** Small municipalities and
municipal-service organizations in Bangladesh.

**Problem addressed:** Manual complaint tracking,
repetitive service questions, and fragmented guidance.

**Proposed business model:** One-time setup fee plus
annual hosting, support, and maintenance.

**Value proposition:** A centralized complaint workflow
and AI-assisted access to service information.

This is a proposed commercial model, not an existing
government partnership or paying-customer claim.

## 12. Submission links

Replace these placeholders before submission:

**GitHub repository:** ADD_PUBLIC_GITHUB_REPOSITORY_URL

**Demonstration video (Google Drive):**
ADD_PUBLIC_GOOGLE_DRIVE_VIDEO_URL

**Live backend Swagger on Render:**
ADD_LIVE_RENDER_DOCS_URL

Make the repository accessible and the Google Drive
video viewable to anyone with the link.

## 13. Demonstration video plan

Record a 5–10 minute demonstration in your own voice.

Include:
1. Project overview, users, problem, and features
2. Domain API data flow
3. Chat and tool-calling data flow
4. RAG ingestion and retrieval data flow
5. MCP tool/resource/prompt data flow
6. JWT authentication and authorization data flow
7. Working frontend and admin demonstration
8. Important backend code explanation

## 14. Security notes

- Do not commit `.env` or `.env.docker`
- Do not commit real API keys or JWT secrets
- Passwords are stored using secure hashes
- Roles are checked on the backend
- Admin promotion is an authorized local operation
- This application is not a government authority
