from models.brand_dna import BrandDNA


def build_rewrite_prompt(
    brand_dna: BrandDNA,
    content: str,
) -> str:
    return f"""
You are a brand content optimization expert.

Your task is to rewrite the content so that it aligns more strongly with the Brand DNA.

BRAND DNA:
{brand_dna.model_dump_json(indent=2)}

ORIGINAL CONTENT:
{content}

Requirements:
- Preserve meaning.
- Improve brand alignment.
- Strengthen personality.
- Improve communication style.
- Increase distinctiveness.
- Reduce generic wording.
- Keep professional tone.

Return JSON only:

{{
  "rewritten_content": "string",
  "improvement_summary": [
      "string"
  ]
}}
"""
