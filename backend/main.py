import logging
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")

from schemas.request import AnalyzeRequest
from schemas.response import AnalyzeResponse, SentimentBreakdown
from graph import graph

load_dotenv()

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
    try:
        result = graph.invoke({"youtube_url": body.youtube_url})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return AnalyzeResponse(
        reception_label=result["reception_label"],
        sentiment=SentimentBreakdown(**result["sentiment"]),
        complaints=result["complaints"],
        highlights=result["highlights"],
        summary=result["summary"],
        comments_analyzed=len(result["comments"]),
    )
