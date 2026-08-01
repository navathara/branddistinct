"""
evaluation_prompt.py

Prompt templates for the Evaluation Engine.

Per the developer handbook, this file contains ONLY prompt text and
formatting — no scoring, no business decisions, no JSON parsing.
services/evaluation_service.py sends these prompts to Claude and is
responsible for validating and interpreting the responses.

Two prompts live here, matching the two AI-powered steps in
03_evaluation_pipeline.yaml:

  - build_relevance_check_prompt   -> step_4 (Relevance Check)
  - build_content_evaluation_prompt -> step_5 (BDSF Evaluation:
    dimension_evaluation + genericness_analysis, per
    04_bdsf_methodology.yaml)

Per Principle 1 in the developer handbook, the content-evaluation
prompt asks for per-dimension scores, reasoning, and evidence ONLY —
it never asks Claude to compute the final weighted Brand
Distinctiveness Score or the genericness penalty; those are
calculated deterministically in core/bdsf_scoring.py and
core/genericness.py.
"""

from models.brand_dna import BrandDNA

# ---------------------------------------------------------------------------
# Shared brand context formatting
# ---------------------------------------------------------------------------


def _format_brand_dna_summary(brand_dna: BrandDNA) -> str:
    """
    Renders a BrandDNA object as a compact, readable text block for
    inclusion in a prompt. Pure string templating — used by both
    prompts below so the brand context looks identical across calls.
    """
    identity = brand_dna.identity
    personality = brand_dna.personality
    communication = brand_dna.communication
    audience = brand_dna.audience
    visual = brand_dna.visual_identity
    values = brand_dna.values

    return f"""Brand Name: {identity.brand_name or "Unknown"}
Industry: {identity.industry or "Unknown"}
Mission: {identity.mission or "Not specified"}
Positioning: {identity.positioning or "Not specified"}

Personality Traits: {", ".join(personality.primary_traits) or "Not specified"}
Emotional Style: {personality.emotional_style or "Not specified"}
Brand Archetype: {personality.brand_archetype or "Not specified"}

Tone of Voice: {communication.tone_of_voice or "Not specified"}
Messaging Pillars: {", ".join(communication.messaging_pillars) or "Not specified"}
Preferred Vocabulary: {", ".join(communication.preferred_vocabulary) or "Not specified"}
Restricted Vocabulary: {", ".join(communication.restricted_vocabulary) or "Not specified"}

Primary Audience Segments: {", ".join(audience.primary_segments) or "Not specified"}
Audience Interests: {", ".join(audience.interests) or "Not specified"}

Primary Colors: {", ".join(visual.primary_colors) or "Not specified"}
Imagery Style: {visual.imagery_style or "Not specified"}

Core Values: {", ".join(values.core_values) or "Not specified"}
Brand Promises: {", ".join(values.brand_promises) or "Not specified"}
Differentiators: {", ".join(values.differentiators) or "Not specified"}"""


# ---------------------------------------------------------------------------
# Step 4: Relevance Check
# ---------------------------------------------------------------------------


def build_relevance_check_prompt(brand_dna: BrandDNA, content: str) -> str:
    """
    Builds a cheap, focused prompt that classifies whether content is
    relevant to the brand before spending a full evaluation call on
    it (03_evaluation_pipeline.yaml step_4).
    """
    brand_summary = _format_brand_dna_summary(brand_dna)
    return f"""You are checking whether a piece of content is relevant to a specific brand before it is evaluated for brand alignment.

Brand Profile:
{brand_summary}

Content to check:
\"\"\"
{content}
\"\"\"

Classify the content's relevance to this brand as exactly one of: "relevant", "partially_relevant", "irrelevant".

- "relevant": the content is clearly about this brand, its products, or its category.
- "partially_relevant": the content is loosely related or generic but not off-topic.
- "irrelevant": the content has nothing to do with this brand or its industry.

Respond with ONLY a JSON object in this exact format, no markdown fences, no commentary:
{{
  "relevance": "relevant",
  "reasoning": "One short sentence explaining the classification."
}}
"""


# ---------------------------------------------------------------------------
# Step 5: BDSF Evaluation (dimension scoring + genericness signal detection)
# ---------------------------------------------------------------------------

_DIMENSION_RESULT_TEMPLATE = """{
    "score": 0,
    "reasoning": "",
    "evidence": {
      "matched_attributes": [],
      "conflicting_attributes": [],
      "supporting_examples": []
    }
  }"""

_RESPONSE_JSON_TEMPLATE = f"""{{
  "identity": {_DIMENSION_RESULT_TEMPLATE},
  "personality": {_DIMENSION_RESULT_TEMPLATE},
  "communication": {_DIMENSION_RESULT_TEMPLATE},
  "audience": {_DIMENSION_RESULT_TEMPLATE},
  "visual_identity": {_DIMENSION_RESULT_TEMPLATE},
  "values": {_DIMENSION_RESULT_TEMPLATE},
  "genericness_signals": {{
    "cliches": [],
    "vague_claims": [],
    "interchangeable_phrases": []
  }}
}}"""


def build_content_evaluation_prompt(brand_dna: BrandDNA, content: str) -> str:
    """
    Builds the prompt that asks Claude to score content against each
    of the six canonical Brand DNA dimensions (01_brand_dna.yaml) and
    separately flag generic-language signals, per
    04_bdsf_methodology.yaml's dimension_evaluation and
    genericness_analysis.
    """
    brand_summary = _format_brand_dna_summary(brand_dna)
    return f"""You are a brand evaluation analyst. Evaluate how well the content below aligns with the brand profile, across each of the six brand dimensions listed.

Brand Profile:
{brand_summary}

Content to evaluate:
\"\"\"
{content}
\"\"\"

For EACH of the six dimensions below, compare the content against the corresponding part of the brand profile and produce a score from 0 (no alignment) to 100 (perfect alignment), one sentence of reasoning, and supporting evidence:

- identity: does the content reflect the brand's mission, positioning, and industry?
- personality: does the content's tone reflect the brand's personality traits and archetype?
- communication: does the content match the brand's tone of voice, messaging pillars, and vocabulary rules?
- audience: does the content speak to the brand's intended audience and their needs?
- visual_identity: does any described visual/stylistic language match the brand's visual identity? (score based on textual/stylistic cues only; if content contains no visual cues, score conservatively and note this in reasoning)
- values: does the content reflect the brand's core values, promises, and differentiators?

Additionally, separately identify any generic marketing language in the content — clichés, vague unsupported claims, and interchangeable phrases that could apply to almost any brand. List each instance found; do not summarize or count them yourself.

Respond with ONLY a JSON object in EXACTLY this structure (no markdown fences, no extra commentary, no missing keys):

{_RESPONSE_JSON_TEMPLATE}

Rules:
- Every "score" must be an integer or float between 0 and 100.
- Every evidence list should contain short, specific items grounded in the actual content and brand profile — do not invent facts.
- If a dimension has no clear evidence either way, use a mid-range score (40-60) and explain why in reasoning.
- Output must be valid, parseable JSON and nothing else.
"""
