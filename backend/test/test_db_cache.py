
import os
import pytest
from app.sitesense.services.chat_cache import SiteSenseCache

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(), override=True)


@pytest.fixture
def cache():
    conn_url = os.getenv("TEST_DB_CACHE")
    cache = SiteSenseCache(conn_url)

    # Cleanup before and after each test
    with cache.conn.cursor() as cur:
        cur.execute("DELETE FROM sitesense_cache;")

    yield cache

    with cache.conn.cursor() as cur:
        cur.execute("DELETE FROM sitesense_cache;")


def test_update_and_lookup(cache):
    prompt = "What is the capital of France?"
    response = "Paris"

    cache.update(prompt, response)
    result = cache.lookup(prompt)

    assert result == response


def test_lookup_returns_none_on_miss(cache):
    prompt = "This prompt does not exist in cache"

    result = cache.lookup(prompt)

    assert result is None
