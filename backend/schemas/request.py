from pydantic import BaseModel, HttpUrl


class AnalyzeRequest(BaseModel):
    youtube_url: str
