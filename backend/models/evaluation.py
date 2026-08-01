"""
evaluation.py

Pydantic schemas for the Evaluation Engine.

Three groups of schemas live here, per the developer handbook
("models contain only schemas"):

1. API request/response schemas for Endpoint 2 (POST /api/evaluate)
   in 08_api_contracts.md.
2. AI-structured-output schemas — the exact shape Gemini is asked to
   return for the relevance check and the content evaluation calls
   (see prompts/relevance_check_prompt.py and
   prompts/content_evaluation_prompt.py).
3. BDSF-specific schemas (BDSFDimensionScores, evidence matrix
   entries) matching 02_bdsf.yaml and 04_bdsf_methodology.yaml.

Architecture note on EvaluateRequest.brand_dna:
    08_api_contracts.md's request example only carries `brand_id`.
    That implies a server-side lookup of the previously-discovered
    BrandDNA — but persistence/database is explicitly out of scope
    for this project. Since there is nowhere to resolve brand_id
    into a BrandDNA object, this request schema adds an explicit
    `brand_dna` field so the caller (which already has it from the
    Brand Discovery + Review steps) can supply it directly. `brand_id`
    is kept for forward compatibility so this field can be dropped
    once persistence exists without another breaking change.
"""

from typing import Literal

from pydantic import BaseModel, Field

from models.brand_dna import BrandDNA


# ---------------------------------------------------------------------------
# API schemas — Endpoint 2 in 08_api_contracts.md
# ---------------------------------------------------------------------------


class EvaluateRequest(BaseModel):
    """Request body for POST /api/evaluate."""

    brand_id: str = Field(..., min_length=1)
    content_type: str = Field(..., min_length=1, examples=["text"])
    content: str = Field(..., min_length=1)
    brand_dna: BrandDNA = Field(
        ...,
        description=(
            "The BrandDNA to evaluate against. Required in place of a "
            "server-side brand_id lookup because no database exists yet."
        ),
    )


class BDSFDimensionScores(BaseModel):
    """
    The five weighted BDSF dimensions, per 02_bdsf.yaml `dimensions`.
    Field names match the API contract's Success Response example
    exactly.
    """

    identity_alignment: int = Field(ge=0, le=100)
    distinctiveness: int = Field(ge=0, le=100)
    consistency: int = Field(ge=0, le=100)
    audience_resonance: int = Field(ge=0, le=100)
    values_alignment: int = Field(ge=0, le=100)


class EvidenceMatrixEntry(BaseModel):
    """
    Per-dimension evidence, per 04_bdsf_methodology.yaml
    `evidence_matrix.generated_for_each_dimension`.
    """

    matched_attributes: list[str] = Field(default_factory=list)
    conflicting_attributes: list[str] = Field(default_factory=list)
    supporting_examples: list[str] = Field(default_factory=list)


class RecommendationsPlaceholder(BaseModel):
    """
    Empty structure — Recommendation Generation (step_7) is out of
    scope for this task. Kept as a field (rather than omitted) to
    preserve the response schema defined in 08_api_contracts.md.
    """

    quick_fixes: list[str] = Field(default_factory=list)
    strategic_improvements: list[str] = Field(default_factory=list)


class EvaluationData(BaseModel):
    """`data` payload for a successful /api/evaluate response."""

    overall_score: int = Field(ge=0, le=100)
    dimension_scores: BDSFDimensionScores
    genericness_penalty: int = Field(ge=0, le=10)
    evaluation_confidence: float = Field(ge=0.0, le=1.0)
    evidence_matrix: dict[str, EvidenceMatrixEntry]
    recommendations: RecommendationsPlaceholder
    warnings: list[str] = Field(
        default_factory=list,
        description=(
            "Non-fatal issues surfaced during evaluation: a "
            "'partially_relevant' relevance outcome (continue_with_warning) "
            "and/or low evaluation_confidence, per "
            "03_evaluation_pipeline.yaml's warning_conditions. Additive "
            "field per the contract's 'extend responses only when "
            "necessary' policy — absent/empty for a clean evaluation."
        ),
    )


# ---------------------------------------------------------------------------
# AI-structured-output schemas
# ---------------------------------------------------------------------------


class RelevanceCheckResult(BaseModel):
    """
    Structured output of the Relevance Check step
    (03_evaluation_pipeline.yaml step_4). Only the classification and
    a short reason — no scoring, no business decision. The service
    layer decides what "irrelevant" vs "partially_relevant" means for
    control flow.
    """

    relevance: Literal["relevant", "partially_relevant", "irrelevant"]
    reasoning: str


class DimensionEvidence(BaseModel):
    """Raw evidence for a single canonical dimension, as returned by Gemini."""

    matched_attributes: list[str] = Field(default_factory=list)
    conflicting_attributes: list[str] = Field(default_factory=list)
    supporting_examples: list[str] = Field(default_factory=list)


class CanonicalDimensionResult(BaseModel):
    """
    AI-generated result for a single canonical Brand DNA dimension,
    per 04_bdsf_methodology.yaml `dimension_evaluation.process`
    (generate_reasoning, collect_evidence, assign_dimension_score).
    """

    score: float = Field(ge=0, le=100)
    reasoning: str
    evidence: DimensionEvidence


class GenericnessSignals(BaseModel):
    """
    Raw genericness indicators detected by the AI, per 02_bdsf.yaml
    `genericness_penalty.indicators`. Deliberately NOT a penalty
    value — per Principle 1 in the developer handbook, the LLM
    detects signals; core/genericness_penalty.py converts them into
    the actual point deduction.
    """

    cliches: list[str] = Field(default_factory=list)
    vague_claims: list[str] = Field(default_factory=list)
    interchangeable_phrases: list[str] = Field(default_factory=list)


class ContentEvaluationResult(BaseModel):
    """
    Full structured output expected from the content-evaluation
    Gemini call: one CanonicalDimensionResult per canonical Brand DNA
    dimension (01_brand_dna.yaml), plus genericness signals.
    """

    identity: CanonicalDimensionResult
    personality: CanonicalDimensionResult
    communication: CanonicalDimensionResult
    audience: CanonicalDimensionResult
    visual_identity: CanonicalDimensionResult
    values: CanonicalDimensionResult
    genericness_signals: GenericnessSignals
