from pydantic import BaseModel


class SentimentBreakdown(BaseModel):
    positive: float
    neutral: float
    negative: float


class AnalyzeResponse(BaseModel):
    reception_label: str
    sentiment: SentimentBreakdown
    complaints: list[str]
    highlights: list[str]
    summary: str
    comments_analyzed: int
