"""
config.py

Centralized application configuration.

Loads environment variables using Pydantic Settings and exposes a
single `settings` object that is imported everywhere else in the
application.

Rule: this is the ONLY module allowed to read environment variables
directly. Every other module (routes, services, core, utils) must
import `settings` from here instead of calling os.getenv() itself.
This keeps configuration centralized, testable, and easy to mock.
"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # --- Application Metadata ---
    app_name: str = "BrandDistinct AI"
    app_version: str = "1.0.0"
    environment: str = "development"  # development | staging | production
    debug: bool = True

    # --- API Configuration ---
    api_prefix: str = "/api"

    # --- CORS ---
    # Comma/JSON-list of origins allowed to call the API from the frontend.
    allowed_origins: list[str] = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

    claude_api_key: str = ""
    claude_model: str = "claude-sonnet-4-20250514"

    # --- Brand Discovery Engine ---
    # Minimum cleaned-content length (characters) required to attempt
    # extraction; below this, the site is treated as having
    # insufficient brand information. Kept configurable per the
    # handbook's "treat thresholds as configurable" mentor policy.
    min_content_length: int = 200
    # Cap on cleaned content sent to Gemini, to keep prompts small
    # and predictable in cost/latency.
    max_extraction_content_chars: int = 6000

    # Weights used to combine completeness-of-extraction and
    # source-content-quality into a single extraction_confidence
    # score (see core/extraction_confidence.py). Must sum to 1.0.
    extraction_confidence_completeness_weight: float = 0.7
    extraction_confidence_source_quality_weight: float = 0.3

    # --- Evaluation Engine: genericness penalty ---
    # Points deducted per detected generic-language indicator
    # (cliché, vague claim, interchangeable phrase). The overall cap
    # of 10 is fixed by 02_bdsf.yaml's genericness_penalty.maximum_deduction
    # and is NOT configurable here, since it's part of the frozen
    # BDSF framework rather than an implementation threshold.
    genericness_points_per_indicator: float = 1.5

    # --- Evaluation Engine: evaluation confidence ---
    # Weights combining evidence strength and scoring consistency
    # into evaluation_confidence (04_bdsf_methodology.yaml
    # confidence.evaluation_confidence.based_on). Must sum to 1.0.
    evaluation_confidence_evidence_weight: float = 0.6
    evaluation_confidence_consistency_weight: float = 0.4

    # Below this per-dimension score standard deviation, scoring is
    # considered maximally consistent; at or above it, consistency is
    # scored 0. Chosen as a generous-but-meaningful spread (a third
    # of the 0-100 score range) rather than a spec-fixed value, which
    # is why it's a tunable setting rather than a BDSF-framework
    # constant.
    evaluation_confidence_max_stdev: float = 35.0

    # Minimum content length (characters, after stripping whitespace)
    # required to attempt evaluation at all. Lower than Brand
    # Discovery's threshold since evaluated content can legitimately
    # be short (e.g. a social media caption), per
    # 05_multimodal_evaluation.md's supported text examples.
    evaluation_min_content_length: int = 15

    # Below this evaluation_confidence, a warning is attached to the
    # response instead of failing the request, per
    # 03_evaluation_pipeline.yaml's warning_conditions
    # (low_evaluation_confidence) and its accompanying note.
    evaluation_confidence_warning_threshold: float = 0.5

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """
    Returns a cached Settings instance.

    lru_cache guarantees the .env file is parsed once and the same
    Settings object is reused everywhere, while still being
    dependency-injectable via FastAPI's Depends(get_settings) in
    routes/services that need it explicitly (e.g. for testing with
    overridden settings).
    """
    return Settings()


# Module-level singleton for simple, direct imports:
#   from config import settings
settings = get_settings()
