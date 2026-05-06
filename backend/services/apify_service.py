import os
import json
import time
import logging
from apify_client import ApifyClient

logger = logging.getLogger(__name__)


class ApifyService:
    _cache = {}
    _cache_ttl = 3600  # 1 hour in seconds

    def __init__(self):
        token = os.getenv("APIFY_API_TOKEN")
        if not token:
            raise RuntimeError("APIFY_API_TOKEN environment variable not set")
        self._client = ApifyClient(token)

    @classmethod
    def _get_cache_key(cls, run_input: dict) -> str:
        """Generate cache key from run_input (typically contains the video URL)."""
        return json.dumps(run_input, sort_keys=True)

    @classmethod
    def _is_cache_valid(cls, cached_at: float) -> bool:
        """Check if cached data is still fresh."""
        return time.time() - cached_at < cls._cache_ttl

    def run_and_fetch(self, actor_id: str, run_input: dict, max_items: int = 100) -> list[dict]:
        cache_key = self._get_cache_key(run_input)

        # Check cache
        if cache_key in self._cache:
            cached_data, cached_at = self._cache[cache_key]
            if self._is_cache_valid(cached_at):
                age = time.time() - cached_at
                logger.info("Cache HIT for actor=%s input=%s (age=%.0fs, %d items)", actor_id, run_input, age, len(cached_data))
                return cached_data
            else:
                logger.info("Cache EXPIRED for actor=%s input=%s", actor_id, run_input)
        else:
            logger.info("Cache MISS for actor=%s input=%s", actor_id, run_input)

        # Fetch fresh data
        run = self._client.actor(actor_id).call(run_input=run_input)
        dataset_id = run["defaultDatasetId"]
        items = list(
            self._client.dataset(dataset_id).iterate_items(limit=max_items)
        )
        logger.info("Fetched %d items from Apify actor=%s, caching result", len(items), actor_id)

        # Cache the result
        self._cache[cache_key] = (items, time.time())

        return items

    @classmethod
    def clear_cache(cls) -> None:
        """Clear all cached data."""
        cls._cache.clear()

    @classmethod
    def set_cache_ttl(cls, ttl_seconds: int) -> None:
        """Set the cache TTL in seconds."""

        cls._cache_ttl = ttl_seconds