import time
from threading import Lock

# Cache lifetime (10 minutes)
CACHE_TTL = 600

# Thread-safe cache
_cache = {}
_lock = Lock()


def get_cached_response(question):
    """
    Return cached response if it exists and has not expired.
    """

    key = question.lower().strip()

    with _lock:

        item = _cache.get(key)

        if item is None:
            return None

        answer, timestamp = item

        if time.time() - timestamp > CACHE_TTL:
            del _cache[key]
            return None

        return answer


def save_cached_response(question, answer):
    """
    Save a response to the cache.
    """

    key = question.lower().strip()

    with _lock:
        _cache[key] = (answer, time.time())


def clear_cache():
    """
    Remove all cached responses.
    """

    with _lock:
        _cache.clear()


def cache_size():
    """
    Return the number of cached items.
    """

    with _lock:
        return len(_cache)
