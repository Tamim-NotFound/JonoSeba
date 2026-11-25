
# JonoSeba (জনসেবা)

### AI-Powered Smart Citizen Services and Complaint Management Platform

JonoSeba is a Bangladesh-focused citizen-service and complaint-management platform. 

It combines **FastAPI, PostgreSQL, pgvector, Google Gemini, RAG, MCP, JWT authentication, Docker, and React** to provide a unified municipal service experience.

Citizens can submit complaints, track their progress, and receive AI-assisted guidance about municipal services.

Administrators can manage complaints, departments, and citizen-service operations.

> **Project notice:** JonoSeba is an independent educational demonstration project. It is not operated by a municipality or government agency.

---

## 1. Project Overview

### The Problem

Citizens in Bangladesh often face difficulties when accessing municipal services.

Common challenges include:

- Finding information about required service documents
- Understanding service application procedures
- Submitting complaints to the appropriate department
- Tracking complaint progress
- Receiving timely responses to common questions
- Managing municipal records through disconnected systems

Municipal service teams also spend time manually handling repetitive queries and maintaining complaint records.

### Our Solution

JonoSeba provides a centralized digital platform connecting citizens, administrators, and AI-assisted municipal service information.

The system supports:

1. Citizen registration and authentication
2. Municipal department information
3. Complaint submission and management
4. Complaint progress tracking
5. AI-assisted citizen-service guidance
6. Retrieval-Augmented Generation (RAG)
7. Database-backed AI tool calling
8. Model Context Protocol (MCP)
9. Administrative management and reporting

### Target Users

- Citizens living in municipal areas of Bangladesh
- Small municipalities and municipal administrative teams
- Local citizen-service offices
- Organizations providing municipal support services

---

## 2. Main Features

### 2.1 Citizen Features

Citizens can:

- Create a personal account
- Log in securely using email and password
- View available municipal departments
- Submit complaints
- View their own complaints
- Track complaint status
- Ask questions through the AI chatbot
- Receive guidance based on stored JonoSeba service information

### 2.2 Administrator Features

Authorized administrators can:

- Access administrative functions
- View citizen complaints
- Search and filter complaint records
- Update complaint status
- Manage relevant municipal information
- Review complaint statistics
- Monitor complaint-management activity

Administrative operations are protected by backend role-based authorization.

### 2.3 AI Chatbot Features

JonoSeba uses Google Gemini for conversational AI and tool selection.

The chatbot supports:

- Bangla and English questions
- Multi-turn conversations
- Database-backed tool calling
- Municipal department information
- Personal complaint-status assistance
- Knowledge-base retrieval
- Answers grounded in saved JonoSeba service guides
- Safe fallback when suitable information is unavailable

The chatbot uses saved service information rather than inventing missing service requirements.

### 2.4 RAG Knowledge System

The RAG implementation supports:

- Document ingestion
- Text chunking
- Gemini-generated embeddings
- PostgreSQL pgvector storage
- Semantic similarity search
- Retrieval of matching knowledge chunks
- Responses constructed from retrieved service information
- Fallback when no suitable knowledge is found

The current project includes 10 saved municipal service guides.

### 2.5 MCP Integration

JonoSeba includes an MCP server for exposing application capabilities to compatible MCP clients.

The MCP implementation provides:

- Database-backed tools
- Resources
- Prompts
- HTTP transport
- Standard input/output (stdio) transport

The MCP server uses the application's existing service and database architecture.

---

## 3. Technology Stack

| Component | Technology |
|---|---|
| Programming language | Python 3.12 |
| Backend framework | FastAPI |
| API documentation | Swagger / OpenAPI |
| Database | PostgreSQL 16 |
| Vector database support | pgvector |
| ORM | SQLAlchemy Async |
| Database migrations | Alembic |
| Authentication | JWT |
| Password hashing | Argon2 |
| Input validation | Pydantic |
| Configuration | pydantic-settings |
| AI model | Google Gemini |
| AI embeddings | Gemini Embedding API |
| RAG | Embeddings + pgvector retrieval |
| Tool calling | Gemini function calling |
| MCP | Python MCP SDK |
| Frontend | React |
| Frontend language | TypeScript |
| Frontend build tool | Vite |
| Dependency management | uv |
| Backend testing | pytest |
| Containerization | Docker and Docker Compose |
| Version control | Git and GitHub |

---

## 4. Project Architecture

JonoSeba follows a modular backend architecture.

Main directories:

```text
JonoSeba/
├── app/
│   ├── core/
│   ├── db/
│   ├── integrations/
│   │   ├── llm/
│   │   └── mcp/
│   └── modules/
│       ├── auth/
│       ├── complaints/
│       ├── departments/
│       └── knowledge/
├── alembic/
├── frontend/
├── scripts/
├── tests/
├── Dockerfile
├── pyproject.toml
├── uv.lock
├── .env.example
└── README.md
```

The backend separates responsibilities into:

- Controllers and API routes
- Services and business logic
- Repositories and database operations
- Pydantic request/response schemas
- SQLAlchemy database models
- Dependency injection
- External AI and MCP integrations

This separation improves maintainability, testing, and extensibility.

---

## 5. Environment Configuration

### Requirements

For local backend development:

- Python 3.12
- uv
- PostgreSQL with pgvector
- Gemini API credentials
- Git

For Docker-based development:

- Docker
- Docker Compose
- Gemini API credentials

For frontend development:

- Node.js
- npm

### Clone the Repository

```bash
git clone YOUR_PUBLIC_GITHUB_REPOSITORY_URL
cd JonoSeba
```

Replace the repository URL with the actual public GitHub URL.

### Install Python Dependencies

```bash
uv sync --frozen
```

### Configure Environment Variables

Create your local environment file:

```bash
cp .env.example .env
```

Update `.env` with the required application settings.

Examples include:

- DATABASE_URL
- JWT_SECRET_KEY
- GEMINI_API_KEY
- GEMINI_MODEL
- Other settings defined in `.env.example`

Use the exact variable names from the project's configuration files.

Never commit real credentials or secret keys.

### Database Configuration

For a locally installed PostgreSQL database, create the project database and enable pgvector.

Example SQL:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

The extension must be enabled in the database used by JonoSeba.

### Run Alembic Migrations

```bash
uv run alembic upgrade head
```

### Seed Municipal Departments

```bash
uv run python -m scripts.seed_departments
```

### Start the Backend

```bash
uv run uvicorn app.main:app --reload --port 8000
```

### Open Swagger Documentation

```text
http://127.0.0.1:8000/docs
```

All main application API endpoints use the `/api/v1` prefix.

---

## 6. Docker Setup

Docker Compose provides the local container environment for JonoSeba.

The existing project setup includes:

- FastAPI backend container
- PostgreSQL with pgvector
- MCP HTTP service

Gemini and its embedding API are accessed through configured external API credentials.

### Step 1: Configure Environment

Create the local `.env` file:

```bash
cp .env.example .env
```

Provide the required credentials and application configuration.

Create a separate `.env.docker` file containing the Docker Compose configuration values.

For example:

```dotenv
POSTGRES_PASSWORD=REPLACE_WITH_A_STRONG_RANDOM_PASSWORD
```

Add any other environment variables required by your actual Docker Compose configuration.

Ensure the Docker database connection settings match the PostgreSQL credentials and service name.

Do not commit `.env` or `.env.docker`.

### Step 2: Build and Start Docker Services

From the project root:

```bash
docker compose --env-file .env.docker up -d --build
```

### Step 3: Check Running Containers

```bash
docker compose --env-file .env.docker ps
```

The backend, database, and MCP services should be running.

### Step 4: Check API Logs

```bash
docker compose --env-file .env.docker logs api --tail=100
```

The current API container startup configuration runs Alembic migrations.

For a manually started environment, migrations can also be applied using the configured application environment.

### Step 5: Seed Departments

```bash
docker compose --env-file .env.docker exec -T api \
  python -m scripts.seed_departments
```

### Step 6: Ingest Saved JonoSeba Research

```bash
docker compose --env-file .env.docker exec -T api \
  python -m scripts.ingest_master_research --all --ingest
```

This ingests the saved municipal service guides into the knowledge database.

The ingestion process:

1. Reads the saved guide content
2. Splits the content into chunks
3. Generates embeddings
4. Stores the chunks and vectors in PostgreSQL
5. Makes the saved research available to the research retrieval path

Previously published document records are protected by the ingestion workflow.

### Step 7: Open API Documentation

```text
http://127.0.0.1:8000/docs
```

### Step 8: Check MCP HTTP Service

The local MCP HTTP endpoint is configured at:

```text
http://127.0.0.1:8001/mcp
```

MCP clients should use the protocol's required initialization and message format.

This endpoint is not a regular REST JSON endpoint.

### Stop Docker Services

```bash
docker compose --env-file .env.docker down
```

**Important:** Do not use `docker compose down -v` unless you intentionally want to remove the database volume and its stored data.

---

## 7. Frontend Setup

The frontend is developed using React, TypeScript, and Vite.

### Install Dependencies

From the project root:

```bash
cd frontend
npm install
```

### Start the Development Server

```bash
npm run dev
```

Default development URL:

```text
http://localhost:5173
```

### Production Build

```bash
npm run build
```

The build runs TypeScript checking and generates the production frontend assets.

The frontend communicates with the FastAPI backend through its configured API base URL.

---

## 8. REST API Endpoints

The main backend API uses the following prefix:

```text
/api/v1
```

### Authentication

| Method | Endpoint | Description |
|---|---|---|
| POST | /api/v1/auth/register | Register a citizen |
| POST | /api/v1/auth/login | Log in and receive a JWT |
| GET | /api/v1/auth/me | Get the current authenticated user |

### Municipal Departments

| Method | Endpoint | Description |
|---|---|---|
| GET | /api/v1/departments | List available departments |

Administrative department-management operations are also available according to backend permissions.

### Complaints

| Method | Endpoint | Description |
|---|---|---|
| POST | /api/v1/complaints | Create a complaint |
| GET | /api/v1/complaints | List accessible complaints |
| GET | /api/v1/complaints/{id} | Get one complaint |
| PATCH | /api/v1/complaints/{id} | Update a complaint |
| DELETE | /api/v1/complaints/{id} | Delete a complaint |

Available operations depend on the user's role and the endpoint's authorization rules.

### AI Chat

| Method | Endpoint | Description |
|---|---|---|
| POST | /api/v1/chat | Send a chatbot message |

The full request and response schemas are available in Swagger.

---

## 9. API Request Examples

The examples below assume that the backend is running on:

```text
http://127.0.0.1:8000
```

### 9.1 Register a Citizen

```bash
curl -X POST \
  http://127.0.0.1:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Demo Citizen",
    "email": "citizen@example.com",
    "password": "REPLACE_WITH_A_STRONG_PASSWORD"
  }'
```

Use a valid password that satisfies the backend's password rules.

### 9.2 Login

```bash
curl -X POST \
  http://127.0.0.1:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "citizen@example.com",
    "password": "REPLACE_WITH_A_STRONG_PASSWORD"
  }'
```

A successful login returns an access token.

### 9.3 Authenticated Requests

Store the received JWT in a local shell variable:

```bash
read -r -s -p "JWT access token: " TOKEN
echo
```

Use the token in authorized requests:

```bash
curl \
  http://127.0.0.1:8000/api/v1/auth/me \
  -H "Authorization: Bearer $TOKEN"
```

### 9.4 List Departments

```bash
curl \
  http://127.0.0.1:8000/api/v1/departments
```

### 9.5 Create a Complaint

```bash
curl -X POST \
  http://127.0.0.1:8000/api/v1/complaints \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "title": "Broken streetlight",
    "description": "The streetlight near our road is not working.",
    "location": "Savar, Dhaka",
    "department_id": 1
  }'
```

Replace `department_id` with the ID of an existing active department.

### 9.6 List Complaints

```bash
curl \
  http://127.0.0.1:8000/api/v1/complaints \
  -H "Authorization: Bearer $TOKEN"
```

### 9.7 Get a Specific Complaint

```bash
curl \
  http://127.0.0.1:8000/api/v1/complaints/1 \
  -H "Authorization: Bearer $TOKEN"
```

Replace `1` with an existing accessible complaint ID.

### 9.8 Update a Complaint

For authorized users, use:

```bash
curl -X PATCH \
  http://127.0.0.1:8000/api/v1/complaints/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "status": "resolved"
  }'
```

Use a supported status value from the Swagger schema and an account with update permission.

### 9.9 Delete a Complaint

```bash
curl -X DELETE \
  http://127.0.0.1:8000/api/v1/complaints/1 \
  -H "Authorization: Bearer $TOKEN"
```

Deletion requires the appropriate authorization.

### 9.10 Chat with Gemini

```bash
curl -X POST \
  http://127.0.0.1:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "message": "ট্রেড লাইসেন্স করতে কী কী কাগজপত্র লাগবে?",
    "history": []
  }'
```

### 9.11 Multi-Turn Chat

The chat endpoint accepts previous messages:

```json
{
  "message": "Can you explain the next step?",
  "history": [
    {
      "role": "user",
      "content": "What is a trade license?"
    },
    {
      "role": "model",
      "content": "A trade license is a business licensing document."
    }
  ]
}
```

The application passes the conversation history to the Gemini integration.

---

## 10. RAG Knowledge Base

JonoSeba includes a municipal service knowledge base.

### 10.1 Saved Service Guides

The current master catalog contains 10 guides:

| No. | Municipal service |
|---|---|
| 1 | New birth registration |
| 2 | Birth registration correction |
| 3 | Lost birth certificate reprint |
| 4 | Death registration and death certificate |
| 5 | New trade license and renewal |
| 6 | Citizenship, character and heir certificates |
| 7 | Holding number, ownership changes and holding tax |
| 8 | Building plan approval |
| 9 | New water connection and billing |
| 10 | Health services, EPI and mosquito control |

These guides contain saved JonoSeba service information.

### 10.2 Ingestion Process

The saved service information is processed through the knowledge ingestion system.

```text
Saved service guide
        |
        v
Knowledge document
        |
        v
Text chunking
        |
        v
Gemini embeddings
        |
        v
PostgreSQL + pgvector
```

### 10.3 Knowledge Retrieval

When a user asks a relevant service question:

```text
Citizen question
       |
       v
Gemini chatbot
       |
       v
Knowledge tool call
       |
       v
Question embedding
       |
       v
pgvector similarity search
       |
       v
Matching knowledge chunks
       |
       v
Grounded response
```

The application prioritizes published knowledge when available.

The saved master-guide research is handled through a separate research retrieval path.

For research-based responses, the backend extracts relevant information from the retrieved chunk content and constructs the final answer.

The answer does not need to reproduce an invented fee, requirement, or procedure.

### 10.4 Research Ingestion Command

```bash
docker compose --env-file .env.docker exec -T api \
  python -m scripts.ingest_master_research --all --ingest
```

### 10.5 Example RAG Questions

Examples:

```text
জন্মনিবন্ধনের জন্য কী কী কাগজপত্র লাগবে?
```

```text
মৃত্যু নিবন্ধন করতে কী কী প্রয়োজন?
```

```text
ট্রেড লাইসেন্সের জন্য প্রয়োজনীয় কাগজপত্র কী?
```

```text
নতুন পানি সংযোগ নিতে কী কী কাগজপত্র লাগবে?
```

```text
ওয়ারিশ সনদের জন্য কী কী তথ্য প্রয়োজন?
```

The chatbot uses the corresponding stored service information when relevant chunks are available.

When suitable information is unavailable, it returns an insufficient-information response instead of inventing details.

---

## 11. AI Tool Calling

JonoSeba implements Gemini function calling.

The AI integration declares three tools:

| Tool | Purpose |
|---|---|
| list_departments | Retrieve municipal department information |
| get_my_complaint_status | Retrieve authorized complaint-status information |
| search_published_knowledge | Retrieve relevant knowledge and optionally saved research |

### Tool Calling Flow

```text
Citizen message
      |
      v
FastAPI Chat Endpoint
      |
      v
Gemini Model
      |
      v
Model selects a tool
      |
      v
Tool Executor
      |
      v
Database / Knowledge Service
      |
      v
Tool Result
      |
      v
Final response
```

The tools execute through application code rather than allowing Gemini unrestricted database access.

Personal complaint information is protected through authenticated user context.

---

## 12. Model Context Protocol (MCP)

JonoSeba includes an MCP integration for compatible external AI clients.

The implementation exposes application capabilities through MCP tools, resources and prompts.

### HTTP Transport

Local MCP HTTP endpoint:

```text
http://127.0.0.1:8001/mcp
```

The MCP HTTP service is bound to localhost in the development configuration.

### Stdio Transport

The MCP implementation also supports standard input/output transport.

A compatible MCP client can launch the configured stdio server entrypoint.

The server source is located under:

```text
app/integrations/mcp/
```

### MCP Architecture

```text
MCP Client
    |
    +---- HTTP transport
    |
    +---- stdio transport
             |
             v
       JonoSeba MCP Server
             |
             v
       MCP Tool / Resource / Prompt
             |
             v
       Application Services
             |
             v
          Database
```

MCP operations reuse the application's existing backend functionality.

---

## 13. Authentication and Security

JonoSeba implements JWT authentication and role-based access control.

### Security Features

- Password hashing using Argon2
- JWT access tokens
- Token expiration
- Authenticated user dependencies
- Backend role-based authorization
- Citizen and administrator roles
- Protection of personal complaint records
- Restricted administrative operations
- Pydantic request validation
- Centralized error handling

### Authentication Flow

```text
Citizen registration
        |
        v
Password validation
        |
        v
Argon2 password hash
        |
        v
PostgreSQL user record
        |
        v
Login
        |
        v
Password verification
        |
        v
Expiring JWT
        |
        v
Protected API request
        |
        v
Token and database role validation
```

### Environment Security

Do not commit:

- `.env`
- `.env.docker`
- API credentials
- JWT secret values
- Database passwords
- `.venv/`
- `__pycache__/`
- `node_modules/`

The `.env.example` file should contain safe configuration examples only.

---

## 14. Five Required Data Flows


### 14.1 Domain API Data Flow

```text
Frontend / Client
      |
      v
FastAPI Controller
      |
      v
Dependency Injection
      |
      v
Service Layer
      |
      v
Repository Layer
      |
      v
PostgreSQL
      |
      v
Pydantic Response
```

### 14.2 Gemini and Tool Calling

```text
Citizen Message
      |
      v
Chat Controller
      |
      v
Chat Service
      |
      v
Gemini Integration
      |
      v
Model Tool Selection
      |
      v
Tool Executor
      |
      v
Database-backed Operation
      |
      v
Tool Result / Response
```

### 14.3 RAG Data Flow

```text
Saved Knowledge
      |
      v
Chunking
      |
      v
Embeddings
      |
      v
pgvector Storage

Citizen Question
      |
      v
Embedding + Vector Search
      |
      v
Retrieved Chunks
      |
      v
Grounded Answer / Fallback
```

### 14.4 MCP Data Flow

```text
MCP Client
      |
      v
HTTP / stdio
      |
      v
MCP Server
      |
      v
Tool / Resource / Prompt
      |
      v
Application Service
      |
      v
Database
```

### 14.5 JWT Authentication Data Flow

```text
Register
   |
   v
Password Hashing
   |
   v
Database

Login
   |
   v
Password Verification
   |
   v
JWT Creation
   |
   v
Protected Request
   |
   v
Token + Role Check
   |
   v
Authorized Operation
```

---

## 15. Testing and Quality Assurance

### Backend Automated Tests

Run:

```bash
uv run pytest -q
```

Latest locally verified result:

```text
241 passed
```

### Frontend Production Build

```bash
cd frontend
npm run build
```

Latest locally verified result:

```text
TypeScript build: PASS
Vite production build: PASS
```

### Docker Configuration

```bash
docker compose --env-file .env.docker config -q
```

Latest locally verified result:

```text
Docker Compose configuration: PASS
```

### RAG Integration Testing

The following checks were completed locally:

- Saved research ingestion into PostgreSQL
- Embedding storage in pgvector
- All 10 master guides present
- 15 stored research chunks
- Research chunks remain unpublished
- Relevant guide retrieval
- Responses constructed from retrieved chunk content
- No unrelated guide returned in the tested fallback case
- Real Gemini chatbot answer using the research retrieval flow


### Real HTTP Chatbot Testing

Authenticated requests were tested through the Docker-hosted API for all 10 saved municipal service topics.

Result:

```text
10/10 municipal service chatbot topics: PASS
```

### Additional Checks

- Git whitespace validation
- Tracked-file hygiene check
- Python syntax compilation
- JWT-authenticated request testing
- Error handling and role-based access tests

### Remaining Environment Verification

A completely fresh Git clone with new Docker volumes should be tested before final submission.

The MCP HTTP and stdio capabilities should also be demonstrated with an actual MCP client.

---

## 16. Business Model and Commercial Potential

JonoSeba is designed as a potential digital service platform for small municipalities and citizen-service organizations.

### Target Customers

Potential paying customers include:

- Small municipalities
- Local citizen-service management organizations
- Municipal support service providers
- Administrative teams responsible for complaint management

### Customer Problem

Municipal administrators often rely on manual workflows, spreadsheets, telephone calls, and separate records.

These approaches can create:

- Delayed complaint processing
- Difficulty tracking citizen requests
- Repeated administrative questions
- Disconnected department information
- Poor visibility into complaint progress

### Proposed Revenue Model

JonoSeba could use a business-to-organization model consisting of:

1. One-time software setup and implementation fee
2. Annual hosting and maintenance subscription
3. Optional customization and training fees

Pricing would depend on organization size, hosting requirements, and requested functionality.

### Why Customers Might Pay

JonoSeba provides a combination of features that may reduce repetitive manual work:

- Centralized complaint records
- Citizen self-service tracking
- Department-based complaint management
- AI-assisted service information
- Administrative dashboards
- Expandable API and MCP integrations

### Commercial Status

This is a proposed business model.

JonoSeba does not claim to have existing paying customers, municipal contracts, or institutional partnerships.

---

## 17. GitHub and Code Quality

The project uses Git and GitHub for version control.

Recommended development practices:

- Keep commits small and descriptive
- Use meaningful commit prefixes such as `feat:`, `fix:`, `test:` and `docs:`
- Do not commit environment secrets
- Keep generated files out of version control
- Maintain updated setup documentation
- Test backend changes before pushing
- Verify frontend production builds
- Use migrations for database schema changes


---

## 20. Live Links

### Live Render Swagger Documentation

```text
https://jonoseba-api.onrender.com/docs
```

---

## 21. Project Status

### Completed Locally

- FastAPI backend
- PostgreSQL integration
- Alembic migrations
- Domain API and complaint management
- JWT authentication and authorization
- Gemini chatbot integration
- Database-backed tool calling
- RAG knowledge ingestion
- pgvector retrieval
- 10 saved municipal service guides
- Grounded research-based chatbot responses
- MCP server implementation
- Docker Compose integration
- React frontend
- Backend automated tests
- Frontend production build


---

## 22. Conclusion

JonoSeba demonstrates how modern backend engineering, AI assistance, vector search, and modular application design can improve municipal citizen-service workflows.

The project combines practical complaint management with conversational access to stored service information.

Its architecture is designed for continued development, additional municipal integrations, and potential organizational deployment.

**JonoSeba — Digital Citizen Services Made Simpler.**
