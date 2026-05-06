import os
import time
import logging

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger(__name__)

from schemas.request import AnalyzeRequest
from schemas.response import AnalyzeResponse, SentimentBreakdown
from graph import graph

# Full-pipeline cache (Apify + LLM) keyed by YouTube URL.
# Configurable via ANALYSIS_CACHE_TTL_SECONDS (default: 3600).
_analysis_cache: dict[str, tuple[AnalyzeResponse, float]] = {}
_analysis_cache_ttl: int = int(os.getenv("ANALYSIS_CACHE_TTL_SECONDS", "3600"))

app = FastAPI(title="YouTube Reception Analyzer")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze(body: AnalyzeRequest):
    url = body.youtube_url

    cached = _analysis_cache.get(url)
    if cached:
        response, cached_at = cached
        age = time.time() - cached_at
        if age < _analysis_cache_ttl:
            logger.info("Cache HIT for url=%s (age=%.0fs)", url, age)
            return response
        logger.info("Cache EXPIRED for url=%s", url)

    try:
        result = graph.invoke({"youtube_url": url})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    response = AnalyzeResponse(
        reception_label=result["reception_label"],
        sentiment=SentimentBreakdown(**result["sentiment"]),
        complaints=result["complaints"],
        highlights=result["highlights"],
        summary=result["summary"],
        comments_analyzed=len(result["comments"]),
    )

    _analysis_cache[url] = (response, time.time())
    logger.info("Cache MISS for url=%s — result stored", url)

    return response
