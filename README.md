# YouTube Reception Analyzer

> Built for the [Apify Hackathon](https://apify.com) — May 6, 2026.

Paste a YouTube URL and get an instant structured analysis of how the audience received the **video** and **topic** — separate breakdowns for each with reception label, sentiment percentages, top complaints, highlights, and summary paragraphs.

Built with **Apify** (comment scraping), **LangGraph** (pipeline orchestration), and **Mistral** (structured LLM output).

## How it works

```
POST /analyze (youtube_url)
        │
        ▼
  LangGraph pipeline
        │
        ├─ scrape_comments ─────────────────────┐
        │   Apify: streamers/youtube-comments-  │
        │   scraper (100 comments)              │
        │                                       ▼
        ├─ analyze_comments    analyze_topic
        │   Mistral:           Mistral:
        │   Video/creator      Topic/subject
        │   reception          opinions
        │   (batches of 50)    (batches of 50)
        │         │                   │
        └─────────┼───────────────────┘
                  ▼                   ▼
          generate_report    generate_topic_report
          Summary +          Summary +
          reception label    reception label
                  │                   │
                  └───────┬───────────┘
                          ▼
                  React frontend
                  (two analysis blocks)
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
│   ├── main.py                      # FastAPI app, response mapping
│   ├── graph.py                     # LangGraph StateGraph assembly
│   ├── state.py                     # AnalysisState TypedDict
│   ├── nodes/
│   │   ├── scrape_comments.py       # Apify actor wrapper
│   │   ├── analyze_comments.py      # Video/creator sentiment analysis
│   │   ├── analyze_topic.py         # Topic/subject sentiment analysis
│   │   ├── generate_report.py       # Video reception summary
│   │   └── generate_topic_report.py # Topic reception summary
│   ├── schemas/
│   │   ├── request.py
│   │   ├── response.py              # AnalyzeResponse, AnalysisBlock
│   │   └── analysis.py              # BatchAnalysis, ReportOutput
│   └── services/
│       ├── apify_service.py         # Wraps Apify client
│       └── mistral_service.py       # ChatMistralAI factory
└── frontend/
    ├── src/
    │   ├── App.tsx                  # State machine: idle → loading → result | error
    │   ├── types/report.ts          # TypeScript interfaces
    │   ├── api/analyzeVideo.ts      # POST /analyze
    │   └── components/
    │       ├── ReceptionReport.tsx   # Two AnalysisBlockSection components
    │       ├── SentimentChart.tsx
    │       ├── ReceptionBadge.tsx
    │       ├── ComplaintsList.tsx
    │       └── HighlightsList.tsx
    └── vite.config.ts               # Proxy config
```
