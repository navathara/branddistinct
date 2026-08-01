"""
web_fetcher.py

Generic, reusable helper for fetching the raw HTML of a public URL.

Deliberately has no knowledge of "brands", "discovery", or business
rules — it only validates a URL's shape and performs an HTTP GET
with a sane timeout and user-agent. Any future module that needs to
fetch a web page can reuse this without modification.

Raises plain, built-in/httpx exceptions on failure so callers
(services/) can translate them into domain-specific errors — this
file stays generic per the handbook's "Utilities must remain
generic" rule.
"""

from urllib.parse import urlparse

import httpx

_DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; BrandDistinctAI/1.0; +https://branddistinct.ai)"
}


def is_valid_http_url(url: str) -> bool:
    """Returns True if `url` is a syntactically valid http(s) URL."""
    try:
        parsed = urlparse(url)
    except ValueError:
        return False
    return parsed.scheme in ("http", "https") and bool(parsed.netloc)


async def fetch_html(url: str, timeout_seconds: float = 10.0) -> str:
    """
    Fetches raw HTML for `url`.

    Raises:
        ValueError: if `url` is not a syntactically valid http(s) URL.
        httpx.HTTPError: if the request fails, times out, or the
            server responds with an error status code.
    """
    if not is_valid_http_url(url):
        raise ValueError(f"'{url}' is not a valid http/https URL.")

    async with httpx.AsyncClient(
        timeout=timeout_seconds, headers=_DEFAULT_HEADERS, follow_redirects=True
    ) as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.text
