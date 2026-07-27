# Simple in-memory cache

response_cache = {}


def get_cached_response(question):
    return response_cache.get(question.lower().strip())


def save_cached_response(question, answer):
    response_cache[question.lower().strip()] = answer
