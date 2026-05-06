import re

from state import AnalysisState
from services.apify_service import ApifyService

YOUTUBE_ID_RE = re.compile(
    r"(?:v=|youtu\.be/|embed/|shorts/)([A-Za-z0-9_-]{11})"
)
MAX_COMMENTS = 100


def scrape_comments(state: AnalysisState) -> dict:
    url = state["youtube_url"]
    service = ApifyService()
    comments = service.run_and_fetch(
        actor_id="streamers/youtube-comments-scraper",
        run_input={
            "startUrls": [{"url": url}],
            "sort": "TOP_COMMENTS",
            "maxComments": MAX_COMMENTS,
        },
        max_items=MAX_COMMENTS,
    )
    return {"comments": comments}
