# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

YouTube Reception Analyzer — scrapes YouTube comments via Apify and runs a LangGraph + Mistral pipeline to produce a structured report: overall reception label, sentiment breakdown, top complaints, highlights, and a summary paragraph.

## Development Commands

### Backend (Python + FastAPI + LangGraph)
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env   # fill in APIFY_API_TOKEN and MISTRAL_API_KEY
uvicorn main:app --reload
```
API available at `http://localhost:8000`. Swagger docs at `/docs`.

### Frontend (React + Vite + TypeScript)
```bash
cd frontend
npm install
npm run dev       # dev server at http://localhost:5173 (proxies /analyze → :8000)
npm run build     # production build
npm run lint      # ESLint
```

## Architecture

```
POST /analyze (youtube_url)
        │
        ▼
  LangGraph graph (backend/graph.py)
        │
        ├─ Node 1: scrape_comments   — Apify actor: streamers/youtube-comments-scraper (100 comments)
        ├─ Node 2: analyze_comments  — Mistral structured output (BatchAnalysis), batches of 50
        └─ Node 3: generate_report   — Mistral structured output (ReportOutput): summary + reception_label
        │
        ▼
  AnalyzeResponse → React frontend
```

### Backend layout
- `state.py` — `AnalysisState` TypedDict (shared across all nodes)
- `graph.py` — assembles and compiles the LangGraph `StateGraph`
- `nodes/` — one file per node; each returns a partial state dict
- `services/apify_service.py` — `ApifyService.run_and_fetch()` wraps the Apify client
- `services/mistral_service.py` — `build_mistral_llm()` factory returns `ChatMistralAI`
- `schemas/analysis.py` — `BatchAnalysis` and `ReportOutput` Pydantic models used for LLM structured output

### Frontend layout
- `App.tsx` — state machine: `idle → loading → result | error`
- `api/analyzeVideo.ts` — single fetch call to `POST /analyze`
- `components/` — one file per UI concern (`ReceptionBadge`, `SentimentBars`, `ComplaintsList`, `HighlightsList`, `ReceptionReport`)
- Vite proxy in `vite.config.ts` forwards `/analyze` and `/health` to `:8000`

## Key Patterns

- **SOLID nodes**: each LangGraph node lives in its own file, returns only the state keys it owns, and delegates I/O to `services/`.
- **Structured LLM output**: nodes use `llm.with_structured_output(PydanticModel)` — never parse raw strings.
- **Apify actor id**: `streamers/youtube-comments-scraper`. Input key is `videoUrl` (full YouTube URL).