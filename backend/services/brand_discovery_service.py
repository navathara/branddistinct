"""
brand_discovery_service.py

Brand Discovery Engine — orchestrates the AI-powered pipeline that
turns a website URL into a validated BrandDNA object.

Per the developer handbook, this is where AI reasoning is
coordinated (fetch -> clean -> prompt -> call Gemini -> validate ->
retry). Deterministic decisions (extraction confidence) are
delegated to core/. Low-level I/O (HTTP fetch, HTML cleaning, the
Gemini SDK call) are delegated to utils/, which stay generic and
reusable. Prompt text lives in prompts/, never inline here.
"""

import json
import re
import uuid
from urllib.parse import urlparse

import httpx

from config import settings
from core.exceptions import (
    AIResponseError,
    InsufficientBrandDataError,
    InvalidURLError,
    WebsiteUnreachableError,
)
from core.extraction_confidence import calculate_extraction_confidence
from models.brand_dna import BrandDNA, BrandDiscoveryData
from prompts.brand_discovery_prompt import build_brand_discovery_prompt
from utils.content_cleaner import extract_readable_text
from utils.claude_client import generate_text
from utils.web_fetcher import fetch_html

_MAX_GEMINI_ATTEMPTS = 2  # 1 initial attempt + 1 retry, per spec requirement #9


def _strip_json_fences(raw_text: str) -> str:
    """Removes ```json / ``` fences some LLMs add despite instructions not to."""
    cleaned = raw_text.strip()
    cleaned = re.sub(r"^```(?:json)?", "", cleaned).strip()
    cleaned = re.sub(r"```$", "", cleaned).strip()
    return cleaned


def _parse_brand_dna(raw_text: str) -> BrandDNA | None:
    """
    Attempts to parse and validate Gemini's raw text response as a
    BrandDNA object. Returns None (never raises) on failure, so the
    caller can decide whether to retry — this is the "malformed
    response" detection required by spec item #9.
    """
    try:
        cleaned = _strip_json_fences(raw_text)
        data = json.loads(cleaned)
        return BrandDNA(**data)
    except (json.JSONDecodeError, TypeError, ValueError):
        return None


def _derive_brand_name(website_url: str) -> str:
    """Fallback brand name derived from the domain when Gemini omits it."""
    netloc = urlparse(website_url).netloc or website_url
    domain_label = netloc.replace("www.", "").split(".")[0]
    return domain_label.replace("-", " ").replace("_", " ").title()


async def discover_brand_dna(website_url: str) -> BrandDiscoveryData:
    """
    Runs the full Brand Discovery pipeline for a given website URL.

    Raises:
        InvalidURLError: the URL is not a syntactically valid http(s) URL.
        WebsiteUnreachableError: the website could not be fetched.
        InsufficientBrandDataError: too little content was found to extract from.
        AIResponseError: Gemini failed or returned an invalid response twice.
    """
    # 1-2: Fetch website content
    try:
        html = await fetch_html(website_url)
    except ValueError as exc:
        raise InvalidURLError(str(exc)) from exc
    except httpx.HTTPError as exc:
        raise WebsiteUnreachableError(f"Could not fetch '{website_url}': {exc}") from exc

    # 3-4: Extract + clean content
    content = extract_readable_text(html, max_chars=settings.max_extraction_content_chars)
    if len(content) < settings.min_content_length:
        raise InsufficientBrandDataError(
            "The website does not contain enough content to build a Brand DNA profile."
        )

    # 5: Build prompt
    prompt = build_brand_discovery_prompt(website_url, content)

    # 6-9: Call Gemini, validate, retry once on malformed response
    brand_dna: BrandDNA | None = None
    last_error = ""
    for _ in range(_MAX_GEMINI_ATTEMPTS):
        try:
            raw_response = await generate_text(
                prompt, settings.gemini_api_key, settings.gemini_model
            )
        except RuntimeError as exc:
            last_error = str(exc)
            continue

        brand_dna = _parse_brand_dna(raw_response)
        if brand_dna is not None:
            break
        last_error = "Gemini response was not valid JSON matching the BrandDNA schema."

    if brand_dna is None:
        raise AIResponseError(
            f"Gemini failed to produce a valid BrandDNA object after "
            f"{_MAX_GEMINI_ATTEMPTS} attempt(s): {last_error}"
        )

    # 10: Extraction confidence
    confidence = calculate_extraction_confidence(brand_dna, len(content))

    return BrandDiscoveryData(
        brand_id=str(uuid.uuid4()),
        brand_name=brand_dna.identity.brand_name or _derive_brand_name(website_url),
        brand_dna=brand_dna,
        extraction_confidence=confidence,
    )
