"""
bdsf_scoring.py

Deterministic BDSF scoring: maps the six AI-scored canonical Brand
DNA dimensions onto the five weighted BDSF dimensions, computes the
weighted positive score, and applies the genericness penalty to
produce the final Brand Distinctiveness Score.

No LLM calls happen here. Per Principle 1 in the developer handbook
("AI analyzes. Business logic decides. LLMs must never directly
generate the final Brand Distinctiveness Score."), Gemini only
assigns per-canonical-dimension scores (see
models.evaluation.ContentEvaluationResult) — this module is
responsible for turning those into the actual composite score.
"""

from models.evaluation import BDSFDimensionScores, ContentEvaluationResult

# Weights per 02_bdsf.yaml `dimensions`. Fixed by the canonical BDSF
# framework spec (they sum to 100) — not a tunable threshold, since
# changing them would mean deviating from the frozen framework
# itself rather than tuning an implementation detail.
_WEIGHTS: dict[str, int] = {
    "identity_alignment": 30,
    "distinctiveness": 25,
    "consistency": 20,
    "audience_resonance": 15,
    "values_alignment": 10,
}


def map_to_bdsf_dimensions(evaluation: ContentEvaluationResult) -> BDSFDimensionScores:
    """
    Maps the six canonical dimension scores onto the five BDSF
    dimensions per 02_bdsf.yaml's `mapping` section:

        identity_alignment  <- identity
        distinctiveness     <- avg(personality, communication)
        consistency         <- avg(communication, visual_identity)
        audience_resonance  <- audience
        values_alignment    <- values

    Per the mapping_rule note in 02_bdsf.yaml ("Canonical Brand DNA
    dimensions are evaluated once. The resulting scores may be
    reused across multiple BDSF dimensions where appropriate."),
    `communication` legitimately feeds both distinctiveness and
    consistency without being re-evaluated by the AI a second time.
    """
    return BDSFDimensionScores(
        identity_alignment=round(evaluation.identity.score),
        distinctiveness=round(
            (evaluation.personality.score + evaluation.communication.score) / 2
        ),
        consistency=round(
            (evaluation.communication.score + evaluation.visual_identity.score) / 2
        ),
        audience_resonance=round(evaluation.audience.score),
        values_alignment=round(evaluation.values.score),
    )


def calculate_weighted_score(dimension_scores: BDSFDimensionScores) -> float:
    """
    Weighted sum of the five BDSF dimensions, per 02_bdsf.yaml
    `overall_score.calculation.positive_score`. Since the weights sum
    to 100 and each dimension score is already in [0, 100], the
    result stays within [0, 100] without needing separate
    normalization.
    """
    weighted_sum = sum(
        getattr(dimension_scores, dimension) * weight
        for dimension, weight in _WEIGHTS.items()
    )
    return weighted_sum / 100


def apply_genericness_penalty(positive_score: float, genericness_penalty: int) -> int:
    """
    Final aggregation step, per 02_bdsf.yaml `aggregation.formula`
    and `clamp_range`:

        Final Score = Weighted Dimension Score - Genericness Penalty
        clamped to [0, 100]
    """
    final_score = positive_score - genericness_penalty
    return round(min(max(final_score, 0), 100))
