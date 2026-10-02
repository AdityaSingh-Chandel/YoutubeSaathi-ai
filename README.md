# YouTube Video AI Analyzer — V1

```
React (Vite)  ──►  Node/Express (:4000)  ──►  Python/FastAPI (:8000)  ──►  YouTube transcript + Gemini + FAISS
  UI only          validation, API layer        ALL AI/RAG logic
```

The Gemini key lives only in `ai-service/.env`. React never touches AI logic.

## Run locally (3 terminals)

**1. AI service** (Python 3.10+)
```bash
cd ai-service
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env        # put your GEMINI_API_KEY in it
uvicorn app.main:app --reload --port 8000
```

**2. Node backend** (Node 18+)
```bash
cd backend
npm install
cp .env.example .env
npm run dev
```

**3. Frontend**
```bash
cd frontend
npm install
npm run dev                 # http://localhost:5173
```

## API (Node)
| Method | Path | Body | Returns |
|---|---|---|---|
| POST | `/api/analyze` | `{ "youtube_url" }` | `{ session_id, video{id,title,channel,duration_seconds}, summary, transcript }` |
| POST | `/api/question` | `{ "session_id", "question" }` | `{ answer, grounded }` |
| DELETE | `/api/session/:id` | – | `{ deleted: true }` |

Errors always look like `{ "error": { "code", "message" } }`.

## Gemini calls per action
| Action | Gemini calls |
|---|---|
| Analyze | N embedding batches (100 chunks each) + 1 summary call (more only for very long videos) |
| Ask question | 1 query embedding + 1 answer call |
| Copy Summary / Copy Answer | 0 (browser only) |

## Where each V2+ feature plugs in
- **Auth / credits / payments / MongoDB** → Node (`middleware/`, `services/`). The AI service stays untouched.
- **Saved sessions** → implement a `MongoSessionStore` with the same `put/get/delete` as `InMemorySessionStore` in `ai-service/app/services/session_store.py`. (Persist chunks + embeddings, rebuild FAISS on load.)
- **Multiple AI-service instances** → in-memory sessions are per-process. Before scaling out, swap to a shared store (Redis/Mongo) or use sticky routing.
- **Long videos / concurrency** → `analysis_pipeline.analyze_video` is framework-free; move it to a background worker and make `/analyze` return a job id.
- **Timestamps (V4)** → already stored per chunk (`Chunk.start`); just include them in the QA response.
- **Browser extension / mobile** → call the same Node API.

## Known risks
- `youtube-transcript-api` is unofficial. YouTube often blocks cloud-provider IPs; fine locally, but production will likely need a proxy or a transcript provider. It is isolated in `services/transcript/youtube.py`, so replacing it is a one-file change.
- Model names are configurable in `ai-service/.env`; update them if Google retires the defaults.
