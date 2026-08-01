"""
exceptions.py

Domain-level exceptions for BrandDistinct AI.

These map 1:1 to the error codes defined in 08_api_contracts.md.
They are deliberately deterministic (no LLM calls, no I/O) — they
encode *what a failure means to the business*, not how it was
detected. Low-level layers (utils/) raise generic, built-in
exceptions; the service layer catches those and translates them
into one of these typed exceptions. main.py's global exception
handlers turn any BrandDiscoveryError into the standard
ErrorResponse envelope automatically, so API routes never need
their own try/except blocks.
"""


class BrandDiscoveryError(Exception):
    """Base class for all Brand Discovery domain errors."""

    code: str = "INTERNAL_ERROR"
    status_code: int = 500

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class InvalidURLError(BrandDiscoveryError):
    """Raised when the submitted website URL is not a valid http(s) URL."""

    code = "INVALID_URL"
    status_code = 400


class WebsiteUnreachableError(BrandDiscoveryError):
    """Raised when the website cannot be fetched (timeout, DNS, 4xx/5xx)."""

    code = "WEBSITE_UNREACHABLE"
    status_code = 502


class InsufficientBrandDataError(BrandDiscoveryError):
    """
    Raised when there isn't enough brand information to work with —
    either too little website content to extract from (Brand
    Discovery Engine) or a BrandDNA object too sparse to evaluate
    content against (Evaluation Engine).
    """

    code = "INSUFFICIENT_BRAND_DATA"
    status_code = 422


class AIResponseError(BrandDiscoveryError):
    """Raised when Gemini fails, or its output cannot be validated after a retry."""

    code = "AI_RESPONSE_ERROR"
    status_code = 502


class UnsupportedContentError(BrandDiscoveryError):
    """
    Raised by the Evaluation Engine when content_type isn't
    supported (only "text" is implemented) or the submitted content
    is empty/too short to evaluate. Maps to 03_evaluation_pipeline.yaml's
    `unsupported_content` failure condition.
    """

    code = "INVALID_CONTENT"
    status_code = 400


class IrrelevantContentError(BrandDiscoveryError):
    """
    Raised when submitted content has no meaningful relevance to the
    brand (03_evaluation_pipeline.yaml step_4: irrelevant ->
    stop_evaluation).

    NOTE: 08_api_contracts.md's Error Codes table does not define a
    dedicated code for this failure mode. IRRELEVANT_CONTENT is added
    here as a deliberate, minimal extension — permitted by the
    contract's "Extend responses only when necessary" policy —
    rather than overloading INVALID_CONTENT for two semantically
    different failures (wrong content type vs. off-topic content).
    Flagged for the next spec-consistency audit.
    """

    code = "IRRELEVANT_CONTENT"
    status_code = 422
