"""
evaluation_service.py

Evaluation Engine — orchestrates the AI-powered pipeline that scores
submitted text content against a brand's BrandDNA using the Brand
Distinctiveness Scoring Framework (BDSF).

Flow, per 03_evaluation_pipeline.yaml:

  step_3 (content submission, validated by caller)
  -> step_4  Relevance Check (Gemini)
  -> step_5  BDSF Evaluation: per-dimension scoring +
             genericness signal detection (Gemini)
  -> step_6  Evidence Matrix Generation (core.evidence)
  -> deterministic BDSF scoring, genericness penalty, and
     evaluation confidence (core.bdsf_scoring / core.genericness /
     core.evaluation_confidence)

Recommendation Generation (step_7) and Report Generation (step_8)
are explicitly out of scope for this task — see
models.evaluation.RecommendationsPlaceholder.

Per the developer handbook, this is where AI reasoning is
coordinated; deterministic decisions live in core/, prompt text
lives in prompts/, and the Gemini SDK call itself lives in utils/
(reused as-is from the Brand Discovery Engine).
"""

import json
import re

from config import settings
from core.bdsf_scoring import (
    apply_genericness_penalty,
    calculate_weighted_score,
    map_to_bdsf_dimensions,
)
from core.evaluation_confidence import calculate_evaluation_confidence
from core.evidence import build_evidence_matrix
from core.exceptions import (
    AIResponseError,
    InsufficientBrandDataError,
    IrrelevantContentError,
    UnsupportedContentError,
)
from core.genericness import calculate_genericness_penalty
from models.brand_dna import BrandDNA
from models.evaluation import (
    ContentEvaluationResult,
    EvaluationData,
    RecommendationsPlaceholder,
    RelevanceCheckResult,
)
from prompts.evaluation_prompt import (
    build_content_evaluation_prompt,
    build_relevance_check_prompt,
)
from utils.claude_client import generate_text

_MAX_GEMINI_ATTEMPTS = 2  # 1 initial attempt + 1 retry, consistent with the Brand Discovery Engine

_SUPPORTED_CONTENT_TYPES = {"text"}


def _strip_json_fences(raw_text: str) -> str:
    """Removes ```json / ``` fences some LLMs add despite instructions not to."""
    cleaned = raw_text.strip()
    cleaned = re.sub(r"^```(?:json)?", "", cleaned).strip()
    cleaned = re.sub(r"```$", "", cleaned).strip()
    return cleaned


async def _call_gemini_structured(prompt: str, model_cls: type):
    """
    Sends `prompt` to Gemini, retrying once on a malformed/invalid
    response, and returns a validated instance of `model_cls`.

    Raises:
        AIResponseError: if Gemini fails or returns an invalid
            response on both attempts.
    """
    last_error = ""
    for _ in range(_MAX_GEMINI_ATTEMPTS):
        try:
            raw_response = await generate_text(
                prompt, settings.gemini_api_key, settings.gemini_model
            )
        except RuntimeError as exc:
            last_error = str(exc)
            continue

        try:
            cleaned = _strip_json_fences(raw_response)
            data = json.loads(cleaned)
            return model_cls(**data)
        except (json.JSONDecodeError, TypeError, ValueError):
            last_error = "Gemini response was not valid JSON matching the expected schema."
            continue

    raise AIResponseError(
        f"Gemini failed to produce a valid {model_cls.__name__} after "
        f"{_MAX_GEMINI_ATTEMPTS} attempt(s): {last_error}"
    )


def _has_sufficient_brand_information(brand_dna: BrandDNA) -> bool:
    """
    Minimal sanity check that the BrandDNA carries enough signal to
    evaluate against: a brand name plus at least one other filled
    field across the remaining five dimensions.
    """
    if not brand_dna.identity.brand_name:
        return False

    for section in (
        brand_dna.personality,
        brand_dna.communication,
        brand_dna.audience,
        brand_dna.visual_identity,
        brand_dna.values,
    ):
        if any(value not in (None, "", []) for value in section.model_dump().values()):
            return True
    return False


async def evaluate_content(brand_dna: BrandDNA, content_type: str, content: str) -> EvaluationData:
    """
    Runs the full Evaluation Engine pipeline for a single piece of
    text content against a brand's BrandDNA.

    Raises:
        UnsupportedContentError: content_type isn't "text", or content is empty/too short.
        InsufficientBrandDataError: the BrandDNA is too sparse to evaluate against.
        IrrelevantContentError: content has nothing to do with the brand.
        AIResponseError: Gemini failed or returned an invalid response twice.
    """
    if content_type not in _SUPPORTED_CONTENT_TYPES:
        raise UnsupportedContentError(
            f"Content type '{content_type}' is not supported yet. Only 'text' is implemented."
        )
    if len(content.strip()) < settings.evaluation_min_content_length:
        raise UnsupportedContentError("Content is too short to evaluate.")

    if not _has_sufficient_brand_information(brand_dna):
        raise InsufficientBrandDataError(
            "The provided Brand DNA does not contain enough information to evaluate content against."
        )

    warnings: list[str] = []

    # Step 4: Relevance Check
    relevance_prompt = build_relevance_check_prompt(brand_dna, content)
    relevance_result = await _call_gemini_structured(relevance_prompt, RelevanceCheckResult)

    if relevance_result.relevance == "irrelevant":
        raise IrrelevantContentError(
            f"Content does not appear relevant to this brand: {relevance_result.reasoning}"
        )
    if relevance_result.relevance == "partially_relevant":
        warnings.append(
            f"Content is only partially relevant to the brand: {relevance_result.reasoning}"
        )

    # Step 5: BDSF Evaluation (per-dimension scoring + genericness signal detection)
    evaluation_prompt = build_content_evaluation_prompt(brand_dna, content)
    evaluation_result = await _call_gemini_structured(evaluation_prompt, ContentEvaluationResult)

    # Step 6: Evidence Matrix Generation
    evidence_matrix = build_evidence_matrix(evaluation_result)

    # Deterministic scoring (core/) — Principle 1: AI analyzes, business logic decides.
    bdsf_scores = map_to_bdsf_dimensions(evaluation_result)
    positive_score = calculate_weighted_score(bdsf_scores)
    genericness_penalty = calculate_genericness_penalty(evaluation_result.genericness_signals)
    overall_score = apply_genericness_penalty(positive_score, genericness_penalty)

    evaluation_confidence = calculate_evaluation_confidence(evaluation_result)
    if evaluation_confidence < settings.evaluation_confidence_warning_threshold:
        warnings.append(
            "Evaluation confidence is below the acceptable threshold; "
            "treat this score as indicative, not fully reliable."
        )

    return EvaluationData(
        overall_score=overall_score,
        dimension_scores=bdsf_scores,
        genericness_penalty=genericness_penalty,
        evaluation_confidence=evaluation_confidence,
        evidence_matrix=evidence_matrix,
        recommendations=RecommendationsPlaceholder(),
        warnings=warnings,
    )
