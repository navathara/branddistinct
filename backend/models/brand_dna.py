"""
brand_dna.py

Pydantic schemas for the Brand Discovery Engine.

Two things live here, per the developer handbook ("models contain
only schemas"):

1. BrandDNA and its six canonical sub-schemas — a strict mirror of
   01_brand_dna.yaml's `brand_dna.fields`. No field is invented here
   that isn't in the source-of-truth YAML.
2. The request/response schemas for the Brand Discovery API
   endpoint, matching Endpoint 1 in 08_api_contracts.md.

All BrandDNA leaf fields are Optional with safe defaults. This is a
deliberate choice: a website will rarely contain every possible
branding signal, and the whole point of `extraction_confidence`
(core/extraction_confidence.py) is to measure how *complete* the
extraction turned out to be. Rejecting a response for missing
fields would make that measurement meaningless.
"""

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Canonical Brand DNA dimensions (01_brand_dna.yaml)
# ---------------------------------------------------------------------------


class BrandIdentity(BaseModel):
    brand_name: str | None = None
    industry: str | None = None
    mission: str | None = None
    vision: str | None = None
    positioning: str | None = None


class BrandPersonality(BaseModel):
    primary_traits: list[str] = Field(default_factory=list)
    emotional_style: str | None = None
    brand_archetype: str | None = None


class BrandCommunication(BaseModel):
    tone_of_voice: str | None = None
    messaging_pillars: list[str] = Field(default_factory=list)
    preferred_vocabulary: list[str] = Field(default_factory=list)
    restricted_vocabulary: list[str] = Field(default_factory=list)
    reading_level: str | None = None


class BrandAudience(BaseModel):
    primary_segments: list[str] = Field(default_factory=list)
    demographics: str | None = None
    interests: list[str] = Field(default_factory=list)
    customer_needs: list[str] = Field(default_factory=list)


class VisualIdentity(BaseModel):
    primary_colors: list[str] = Field(default_factory=list)
    imagery_style: str | None = None
    composition_style: str | None = None
    logo_usage: str | None = None


class BrandValues(BaseModel):
    core_values: list[str] = Field(default_factory=list)
    brand_promises: list[str] = Field(default_factory=list)
    differentiators: list[str] = Field(default_factory=list)


class BrandDNA(BaseModel):
    """
    Full Brand DNA profile. Field names and nesting match
    01_brand_dna.yaml exactly — this is the schema all six canonical
    dimensions (identity, personality, communication, audience,
    visual_identity, values) must reference, per that file's
    `evaluation_reference.note`.
    """

    identity: BrandIdentity
    personality: BrandPersonality
    communication: BrandCommunication
    audience: BrandAudience
    visual_identity: VisualIdentity
    values: BrandValues


# ---------------------------------------------------------------------------
# API schemas — Endpoint 1 in 08_api_contracts.md
# ---------------------------------------------------------------------------


class DiscoverRequest(BaseModel):
    """Request body for POST /api/brand/discover."""

    website_url: str = Field(..., min_length=1, examples=["https://company.com"])


class BrandDiscoveryData(BaseModel):
    """
    `data` payload for a successful Brand Discovery response.
    Field names match the contract's Success Response example
    exactly: brand_id, brand_name, brand_dna, extraction_confidence.
    """

    brand_id: str
    brand_name: str
    brand_dna: BrandDNA
    extraction_confidence: float = Field(ge=0.0, le=1.0)
