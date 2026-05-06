import logging
from apify_client import ApifyClient
import os

logger = logging.getLogger(__name__)


class ApifyService:
    def __init__(self):
        token = os.getenv("APIFY_API_TOKEN")
        if not token:
            raise RuntimeError("APIFY_API_TOKEN environment variable not set")
        self._client = ApifyClient(token)

    def run_and_fetch(self, actor_id: str, run_input: dict, max_items: int = 100) -> list[dict]:
        run = self._client.actor(actor_id).call(run_input=run_input)
        dataset_id = run["defaultDatasetId"]
        items = list(
            self._client.dataset(dataset_id).iterate_items(limit=max_items)
        )
        return items
