"""
claude_client.py

Thin, generic async wrapper around the Gemini SDK.

Knows nothing about BrandDNA, prompts, or business rules — it only
sends a prompt string to Gemini and returns the raw text response.
Any future service (e.g. the Evaluation Engine) can reuse this
without modification, per the handbook's "Utilities must remain
generic" rule.

Uses the `google-genai` package (the current, actively maintained
Gemini SDK). The older `google-generativeai` package it replaces has
been deprecated by Google in favor of this unified SDK — using it
here avoids building the internship-track codebase on a dead
dependency.
"""

import asyncio

from anthropic import AsyncAnthropic


async def generate_text(prompt: str, api_key: str, model_name: str) -> str:
    """
    Sends `prompt` to the given Gemini model and returns the raw
    text response.

    Raises:
        RuntimeError: if the API key is missing or the Gemini call
            fails for any reason (invalid key, network error, quota,
            content-safety block, etc.).
    """
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not configured.")

    def _call() -> str:
        client = genai.Client(api_key=api_key)
        response = client.messages.create(model=model_name, contents=prompt)
        return response.content[0].text

    try:
        # The Gemini SDK call is synchronous — run it in a worker
        # thread so it never blocks the FastAPI event loop.
        return await asyncio.to_thread(_call)
    except Exception as exc:
        raise RuntimeError(f"Gemini request failed: {exc}") from exc
