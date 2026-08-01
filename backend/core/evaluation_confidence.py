"""
evaluation_confidence.py

Deterministic calculation of Evaluation Confidence, per
04_bdsf_methodology.yaml:

    confidence.evaluation_confidence.based_on:
      - evidence_strength
      - scoring_consistency

No LLM calls happen here — same pattern as
core/extraction_confidence.py, operating on an already-validated
ContentEvaluationResult rather than raw brand data.
"""

import statistics

from config import settings
from models.evaluation import CanonicalDimensionResult, ContentEvaluationResult


def _canonical_dimensions(evaluation: ContentEvaluationResult) -> list[CanonicalDimensionResult]:
    return [
        evaluation.identity,
        evaluation.personality,
        evaluation.communication,
        evaluation.audience,
        evaluation.visual_identity,
        evaluation.values,
    ]


def _evidence_strength(evaluation: ContentEvaluationResult) -> float:
    """
    Fraction of canonical dimensions that have at least one piece of
    concrete evidence (a matched attribute, a conflicting attribute,
    or a supporting example) backing their score, rather than being
    asserted with nothing to point to. Conflicting attributes still
    count as evidence — they mean the AI found something concrete to
    compare against, even if it didn't align.
    """
    dimensions = _canonical_dimensions(evaluation)
    if not dimensions:
        return 0.0

    supported = sum(
        1
        for dim in dimensions
        if dim.evidence.matched_attributes
        or dim.evidence.conflicting_attributes
        or dim.evidence.supporting_examples
    )
    return supported / len(dimensions)


def _scoring_consistency(evaluation: ContentEvaluationResult) -> float:
    """
    How tightly the six canonical dimension scores cluster together.
    Wildly inconsistent scores across dimensions (e.g. 95, 10, 88, 15)
    suggest a less reliable evaluation than scores that agree with
    each other, even if the underlying reasoning differs per
    dimension.
    """
    scores = [dim.score for dim in _canonical_dimensions(evaluation)]
    if len(scores) < 2:
        return 1.0

    stdev = statistics.pstdev(scores)
    return max(0.0, 1.0 - (stdev / settings.evaluation_confidence_max_stdev))


def calculate_evaluation_confidence(evaluation: ContentEvaluationResult) -> float:
    """
    Returns a confidence score in [0.0, 1.0] combining how well the
    per-dimension scores are backed by evidence with how internally
    consistent those scores are.
    """
    evidence_strength = _evidence_strength(evaluation)
    scoring_consistency = _scoring_consistency(evaluation)

    confidence = (
        settings.evaluation_confidence_evidence_weight * evidence_strength
        + settings.evaluation_confidence_consistency_weight * scoring_consistency
    )
    return round(min(max(confidence, 0.0), 1.0), 2)
