import json
from typing import Any

from config import settings
from models.brand_dna import BrandDNA
from utils.claude_client import generate_text


async def rewrite_content(
    brand_dna: BrandDNA,
    original_content: str,
) -> dict[str, Any]:

    prompt = f"""
You are a brand copywriting expert.

BRAND DNA:
{brand_dna.model_dump_json(indent=2)}

ORIGINAL CONTENT:
{original_content}

TASK:
Rewrite the content so that it:

1. Better reflects the brand personality.
2. Uses preferred vocabulary.
3. Aligns with brand values.
4. Improves audience resonance.
5. Reduces generic language.
6. Maintains the original intent.

Return ONLY valid JSON in this exact format:

{{
  "rewritten_content": "...",
  "improvement_summary": [
    "...",
    "...",
    "..."
  ]
}}

The improvement_summary should contain 3-6 concise bullet points describing the improvements you made.

Do not wrap the JSON in markdown.
Do not include any explanation.
Return only the JSON object.
"""

    response = await generate_text(
        prompt,
        settings.claude_api_key,
        settings.claude_model,
    )

    # Claude sometimes wraps JSON in ```json ... ```
    cleaned = response.strip()

    if cleaned.startswith("```json"):
        cleaned = cleaned[7:]

    if cleaned.startswith("```"):
        cleaned = cleaned[3:]

    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]

    cleaned = cleaned.strip()

    return json.loads(cleaned)
