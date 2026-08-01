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

        return response.content[0].text

    except Exception as exc:
        raise RuntimeError(f"Claude request failed: {exc}") from exc
