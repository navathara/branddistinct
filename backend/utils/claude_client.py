"""
claude_client.py

Thin async wrapper around Anthropic Claude.

Knows nothing about BrandDNA, prompts, or business logic.
It simply sends a prompt to Claude and returns the raw text response.
"""

from anthropic import AsyncAnthropic


async def generate_text(
    prompt: str,
    api_key: str,
    model_name: str,
) -> str:
    """
    Sends a prompt to Claude and returns the raw text response.
    """

    if not api_key:
        raise RuntimeError("CLAUDE_API_KEY is not configured.")

    try:
        client = AsyncAnthropic(api_key=api_key)

        response = await client.messages.create(
            model=model_name,
            max_tokens=4096,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        # Claude may return multiple content blocks:
        # ThinkingBlock, TextBlock, etc.
        # Extract only text blocks.
        text_parts = []

        for block in response.content:
            if hasattr(block, "text"):
                text_parts.append(block.text)

        if not text_parts:
            raise RuntimeError("Claude returned no text content.")

        return "\n".join(text_parts)

    except Exception as exc:
        raise RuntimeError(f"Claude request failed: {exc}") from exc
