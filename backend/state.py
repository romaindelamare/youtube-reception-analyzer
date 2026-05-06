from typing import TypedDict


class AnalysisState(TypedDict):
    youtube_url: str
    comments: list[dict]
    # Video/creator reception
    sentiment: dict          # {positive: float, neutral: float, negative: float}
    complaints: list[str]
    highlights: list[str]
    summary: str
    reception_label: str     # "Positive" | "Mixed" | "Negative"
    # Topic reception
    topic_sentiment: dict
    topic_complaints: list[str]
    topic_highlights: list[str]
    topic_summary: str
    topic_reception_label: str
