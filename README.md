# AI Notes

AI Notes is an asynchronous meeting notes backend. Users upload an audio file, the API creates a processing job, a Celery worker transcribes the audio with Whisper, generates structured notes with Claude, saves the result in PostgreSQL, and exposes job polling endpoints so clients can track progress.

## Tech Stack

- FastAPI
- PostgreSQL / Supabase
- SQLAlchemy
- JWT authentication
- Redis
- Celery
- OpenAI Whisper
- Anthropic Claude
- Pydantic
- Uvicorn

## Architecture
sequenceDiagram
    participant U as User
    participant C as Client
    participant API as FastAPI API
    participant DB as PostgreSQL
    participant R as Redis
    participant W as Celery Worker
    participant WH as Whisper
    participant LLM as Claude

    U->>C: Upload audio
    C->>API: POST /notes with JWT + audio
    API->>DB: INSERT job status=pending
    API->>R: Enqueue process_note(job_id, user_id, audio_path)
    API-->>C: 202 Accepted + job_id

    R->>W: Deliver task
    W->>DB: UPDATE job status=transcribing
    W->>WH: Transcribe audio
    WH-->>W: Transcript

    W->>DB: UPDATE job status=summarising
    W->>LLM: Generate structured notes
    LLM-->>W: Summary + key_points + action_items

    W->>DB: UPDATE job status=saving
    W->>DB: INSERT note
    W->>DB: UPDATE job status=completed, note_id=...

    C->>API: GET /jobs/{job_id}
    API->>DB: Query job
    API-->>C: completed + note_id

    C->>API: GET /notes/{note_id}
    API->>DB: Query note
    API-->>C: Note JSON


flowchart TD
    User[User] --> Client[Client / Swagger / Frontend]
    Client -->|Register / Login| API[FastAPI API]
    Client -->|JWT + audio upload| API

    API -->|Create job| DB[(PostgreSQL / Supabase)]
    API -->|Enqueue process_note task| Redis[(Redis Queue)]

    Redis --> Worker[Celery Worker]

    Worker --> Whisper[Whisper Transcription]
    Whisper --> Worker

    Worker --> Claude[Claude Summarisation]
    Claude --> Worker

    Worker -->|Save note| DB
    Worker -->|Update job status| DB

   Client -->|Poll job status| API
    API -->|Read job / note| DB

## API Endpoints
## API Endpoints

### Health

| Method | Endpoint | Auth | Description |
| --- | --- | --- | --- |
| GET | `/health` | No | Health check |

### Authentication

| Method | Endpoint | Auth | Description |
| --- | --- | --- | --- |
| POST | `/auth/register` | No | Register a new user |
| POST | `/auth/login` | No | Login and receive a JWT access token |

### Notes

| Method | Endpoint | Auth | Description |
| --- | --- | --- | --- |
| POST | `/notes` | Yes | Upload audio and start note processing |
| GET | `/notes` | Yes | List the authenticated user’s notes |
| GET | `/notes/{note_id}` | Yes | Get a specific note |
| DELETE | `/notes/{note_id}` | Yes | Delete a specific note |

### Jobs

| Method | Endpoint | Auth | Description |
| --- | --- | --- | --- |
| POST | `/jobs` | Yes | Create a test job |
| GET | `/jobs/{job_id}` | Yes | Get processing status for a job |

## Running Locally
1. Clone the repo

git clone https://github.com/aad1tshah1/ai_notes.git
cd ai_notes

2. Create and activate a virtual env
python -m venv .venv
source .venv/bin/activate

3. Install dependencies
pip install -r requirements.txt

4. Create .env file
ANTHROPIC_API_KEY=
DATABASE_URL=
SECRET_KEY=
ALGORITHM = 

(You can generate a SECRET_KEY: python -c "import secrets; print(secrets.token_hex(32))")

5. Start Redis server
redis-server

6. Check Redis is running
redis-cli ping

Expected Response:
PONG

6. Start the Celery worker from the backend/
cd backend
celery -A worker.celery_app.celery worker --loglevel=info --pool=solo

(--pool=solo is recommended for local macOS development because Whisper/PyTorch can crash under Celery’s default prefork worker pool.)

7. Start FastAPI
cd backend
python -m uvicorn main:app --reload

8. Open Swagger Docs
http://localhost:8000/docs


## Example Flow
Register a user with POST /auth/register.
Login with POST /auth/login.
Authorize in Swagger using the returned bearer token.
Upload audio with POST /notes.
Copy the returned job_id.
Poll GET /jobs/{job_id} until status is completed.
Use the returned note_id with GET /notes/{note_id}.