from pydantic import BaseModel


class SentimentBreakdown(BaseModel):
    positive: float
    neutral: float
    negative: float


class AnalysisBlock(BaseModel):
    reception_label: str
    sentiment: SentimentBreakdown
    complaints: list[str]
    highlights: list[str]
    summary: str


class AnalyzeResponse(BaseModel):
    video: AnalysisBlock
    topic: AnalysisBlock
    comments_analyzed: int
