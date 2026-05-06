# YouTube Reception Analyzer

> Built for the [Apify Hackathon](https://apify.com) — May 6, 2026.

Paste a YouTube URL and get an instant structured analysis of how the audience received the video — overall reception label, sentiment breakdown, top complaints, highlights, and a summary paragraph.

Built with **Apify** (comment scraping), **LangGraph** (pipeline orchestration), and **Mistral** (structured LLM output).

## How it works

```
POST /analyze (youtube_url)
        │
        ▼
  LangGraph pipeline
        │
        ├─ scrape_comments   — Apify: streamers/youtube-comments-scraper (100 comments)
        ├─ analyze_comments  — Mistral structured output, batches of 50
        └─ generate_report   — Mistral structured output: summary + reception label
        │
        ▼
  React frontend
```

## Prerequisites

- Python 3.11+
- Node.js 18+
- An [Apify](https://apify.com) API token
- A [Mistral](https://mistral.ai) API key

## Setup

### Backend

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env   # fill in APIFY_API_TOKEN and MISTRAL_API_KEY
uvicorn main:app --reload
```

API runs at `http://localhost:8000`. Swagger docs at `/docs`.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

App runs at `http://localhost:5173` and proxies `/analyze` to the backend.

## Project structure

```
├── backend/
│   ├── main.py                  # FastAPI app
│   ├── graph.py                 # LangGraph StateGraph assembly
│   ├── state.py                 # AnalysisState TypedDict
│   ├── nodes/                   # One file per pipeline node
│   ├── schemas/                 # Pydantic models (request, response, LLM output)
│   └── services/
│       ├── apify_service.py     # Wraps Apify client
│       └── mistral_service.py   # ChatMistralAI factory
└── frontend/
    ├── src/
    │   ├── App.tsx              # State machine: idle → loading → result | error
    │   ├── api/analyzeVideo.ts  # POST /analyze
    │   └── components/          # ReceptionBadge, SentimentBars, ComplaintsList, …
    └── vite.config.ts           # Proxy config
```
