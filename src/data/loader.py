import fastf1


def enable_cache(cache_dir: str = "cache") -> None:
    fastf1.Cache.enable_cache(cache_dir)


def load_session(year: int, event: str, session_type: str = "R"):
    session = fastf1.get_session(year, event, session_type)
    session.load()
    return session
