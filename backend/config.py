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
    # Origins allowed to call the API from the frontend.
    allowed_origins: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://branddistinct-pmmcr4gse-branddistinct.vercel.app",
    ]

    # --- Claude Configuration ---
    claude_api_key: str = ""
    claude_model: str = "claude-sonnet-4-20250514"

    # --- Brand Discovery Engine ---
    # Minimum cleaned-content length (characters) required to attempt
    # extraction; below this, the site is treated as having
    # insufficient brand information.
    min_content_length: int = 200

    # Cap on cleaned content sent to Gemini, to keep prompts small
    # and predictable in cost/latency.
    max_extraction_content_chars: int = 6000

    # Weights used to combine completeness-of-extraction and
    # source-content-quality into a single extraction_confidence score.
    # Must sum to 1.0.
    extraction_confidence_completeness_weight: float = 0.7
    extraction_confidence_source_quality_weight: float = 0.3

    # --- Evaluation Engine: genericness penalty ---
    # Points deducted per detected generic-language indicator.
    genericness_points_per_indicator: float = 1.5

    # --- Evaluation Engine: evaluation confidence ---
    # Weights combining evidence strength and scoring consistency.
    # Must sum to 1.0.
    evaluation_confidence_evidence_weight: float = 0.6
    evaluation_confidence_consistency_weight: float = 0.4

    # Below this per-dimension score standard deviation, scoring is
    # considered maximally consistent.
    evaluation_confidence_max_stdev: float = 35.0

    # Minimum content length required to attempt evaluation.
    evaluation_min_content_length: int = 15

    # Below this evaluation_confidence, a warning is attached to the
    # response instead of failing the request.
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
    """
    return Settings()


# Module-level singleton for simple, direct imports:
# from config import settings
settings = get_settings()
