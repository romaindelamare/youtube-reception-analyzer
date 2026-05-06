from typing import TypedDict


class AnalysisState(TypedDict):
    youtube_url: str
    comments: list[dict]
    sentiment: dict          # {positive: float, neutral: float, negative: float}
    complaints: list[str]
    highlights: list[str]
    summary: str
    reception_label: str     # "Positive" | "Mixed" | "Negative"
