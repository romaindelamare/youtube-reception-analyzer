from typing import Literal
from pydantic import BaseModel


class BatchAnalysis(BaseModel):
    sentiments: list[Literal["positive", "neutral", "negative"]]
    complaints: list[str]
    highlights: list[str]


class ReportOutput(BaseModel):
    summary: str
    reception_label: Literal["Positive", "Mixed", "Negative"]
