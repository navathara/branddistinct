"""
content_cleaner.py

Generic HTML -> clean text utility.

Strips non-content tags (script, style, nav, footer, forms), pulls
out the elements most likely to carry meaningful signal (title, meta
description, headings, body copy, list items), and collapses
whitespace.

Has no knowledge of "Brand DNA" or branding — it just turns messy
HTML into a plain-text string. Reusable by any future module that
needs to read website content.
"""

import re

from bs4 import BeautifulSoup

_NOISE_TAGS = ["script", "style", "noscript", "nav", "footer", "form", "svg", "iframe"]


def extract_readable_text(html: str, max_chars: int = 6000) -> str:
    """
    Extracts a clean, truncated plain-text summary of an HTML page.
    """
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(_NOISE_TAGS):
        tag.decompose()

    parts: list[str] = []

    if soup.title and soup.title.string:
        parts.append(soup.title.string.strip())

    meta_description = soup.find("meta", attrs={"name": "description"})
    if meta_description and meta_description.get("content"):
        parts.append(meta_description["content"].strip())

    for heading in soup.find_all(["h1", "h2", "h3"]):
        text = heading.get_text(strip=True)
        if text:
            parts.append(text)

    for element in soup.find_all(["p", "li"]):
        text = element.get_text(strip=True)
        if text:
            parts.append(text)

    combined = "\n".join(parts)
    combined = re.sub(r"\n{2,}", "\n", combined).strip()

    return combined[:max_chars]
