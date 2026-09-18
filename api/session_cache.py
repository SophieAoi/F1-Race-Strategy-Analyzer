from functools import lru_cache

from src.data.loader import enable_cache, load_session

enable_cache("cache")


@lru_cache(maxsize=16)
def get_cached_session(year: int, event: str, session_type: str = "R"):
    """Server-side in-process cache on top of FastF1's own disk cache, so a
    session already loaded by one request doesn't get reprocessed (FastF1's
    lap/timing parsing is the slow part, not just the HTTP fetch) on the next.
    """
    return load_session(year, event, session_type)
