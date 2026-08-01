"""
brand_discovery_prompt.py

Prompt template for extracting a structured BrandDNA object from
website content via Claude.

Per the developer handbook, this file contains ONLY the prompt
text — no business logic, no scoring, no JSON parsing. The service
layer (services/brand_discovery_service.py) sends this prompt to
Claude and is responsible for validating the response.

The JSON template below mirrors 01_brand_dna.yaml exactly (same
keys, same nesting, same six canonical dimensions), so a compliant
Claude response maps directly onto models.brand_dna.BrandDNA.
"""

_BRAND_DNA_JSON_TEMPLATE = """{
  "identity": {
    "brand_name": "",
    "industry": "",
    "mission": "",
    "vision": "",
    "positioning": ""
  },
  "personality": {
    "primary_traits": [],
    "emotional_style": "",
    "brand_archetype": ""
  },
  "communication": {
    "tone_of_voice": "",
    "messaging_pillars": [],
    "preferred_vocabulary": [],
    "restricted_vocabulary": [],
    "reading_level": ""
  },
  "audience": {
    "primary_segments": [],
    "demographics": "",
    "interests": [],
    "customer_needs": []
  },
  "visual_identity": {
    "primary_colors": [],
    "imagery_style": "",
    "composition_style": "",
    "logo_usage": ""
  },
  "values": {
    "core_values": [],
    "brand_promises": [],
    "differentiators": []
  }
}"""


def build_brand_discovery_prompt(website_url: str, website_content: str) -> str:
    """
    Builds the Claude prompt used to extract a BrandDNA object.

    Args:
        website_url: The source URL, given as context to Claude.
        website_content: Cleaned, plain-text website content
            (see utils/content_cleaner.py).
    """
    return f"""You are a brand strategy analyst extracting a structured brand profile from website content.

Source website: {website_url}

Website content:
\"\"\"
{website_content}
\"\"\"

Analyze the content above and produce a BrandDNA JSON object with EXACTLY the following structure and keys (no additional keys, no missing keys):

{_BRAND_DNA_JSON_TEMPLATE}

Rules:
- Respond with ONLY the JSON object. No markdown code fences, no explanation, no preamble, no trailing commentary.
- Use only information that is supported by the website content. Do not invent facts.
- If a field cannot be determined from the content, use an empty string "" or an empty list [], depending on its type. Do not omit the key.
- List fields (e.g. primary_traits, messaging_pillars) should contain 3-7 concise items when the content supports it.
- Keep string fields concise (1-2 sentences maximum).
- Output must be valid, parseable JSON and nothing else.
"""
