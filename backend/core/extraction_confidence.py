"""
extraction_confidence.py

Deterministic calculation of Extraction Confidence, per
04_bdsf_methodology.yaml:

    confidence.extraction_confidence.based_on:
      - completeness_of_brand_information
      - source_quality

No LLM calls happen here — this is pure business logic operating on
an already-validated BrandDNA object and metadata about the source
content. Per Principle 1 in the developer handbook, this is exactly
the kind of decision that must live in core/, not inside a prompt.
"""

from config import settings
from models.brand_dna import BrandDNA

# Thresholds are centralized here, not scattered through the
# service layer, so they can be tuned without touching orchestration
# code. The completeness/source-quality weights themselves live in
# config.py (see settings.extraction_confidence_*_weight) so they
# can be tuned via environment variables without a code change.
_SOURCE_QUALITY_FULL_SCORE_CHARS = 1500
_SOURCE_QUALITY_MIN_CHARS = 200


def _iter_leaf_values(brand_dna: BrandDNA):
    """Yields every leaf field value across all six BrandDNA dimensions."""
    for section in (
        brand_dna.identity,
        brand_dna.personality,
        brand_dna.communication,
        brand_dna.audience,
        brand_dna.visual_identity,
        brand_dna.values,
    ):
        yield from section.model_dump().values()


def _completeness_ratio(brand_dna: BrandDNA) -> float:
    """Fraction of BrandDNA leaf fields that were actually filled in."""
    values = list(_iter_leaf_values(brand_dna))
    if not values:
        return 0.0

    filled = sum(1 for v in values if v not in (None, "", []))
    return filled / len(values)


def _source_quality_score(source_content_length: int) -> float:
    """
    Scores the amount of source content available to extract from,
    scaled linearly between the minimum usable length and a length
    considered "rich enough" for a high-confidence extraction.
    """
    if source_content_length <= _SOURCE_QUALITY_MIN_CHARS:
        return 0.0
    if source_content_length >= _SOURCE_QUALITY_FULL_SCORE_CHARS:
        return 1.0

    span = _SOURCE_QUALITY_FULL_SCORE_CHARS - _SOURCE_QUALITY_MIN_CHARS
    return (source_content_length - _SOURCE_QUALITY_MIN_CHARS) / span


def calculate_extraction_confidence(brand_dna: BrandDNA, source_content_length: int) -> float:
    """
    Returns a confidence score in [0.0, 1.0] combining how complete
    the extracted BrandDNA is with how much source content backed
    the extraction.
    """
    completeness = _completeness_ratio(brand_dna)
    source_quality = _source_quality_score(source_content_length)

    confidence = (
        settings.extraction_confidence_completeness_weight * completeness
        + settings.extraction_confidence_source_quality_weight * source_quality
    )
    return round(min(max(confidence, 0.0), 1.0), 2)
