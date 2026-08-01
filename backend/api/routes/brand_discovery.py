"""
brand_discovery.py

Brand Discovery endpoint — POST /api/brand/discover.

Matches Endpoint 1 in 08_api_contracts.md. This route stays thin
per the developer handbook: it only validates the request shape
(via DiscoverRequest) and delegates all work to the Brand Discovery
service. Every failure mode is raised as a typed exception from
core.exceptions and handled globally by main.py's exception
handlers, so this file never needs its own try/except blocks.
"""

from fastapi import APIRouter

from models.brand_dna import BrandDiscoveryData, DiscoverRequest
from models.response import SuccessResponse
from services.brand_discovery_service import discover_brand_dna

router = APIRouter()


@router.post("/brand/discover", response_model=SuccessResponse[BrandDiscoveryData])
async def discover_brand(payload: DiscoverRequest) -> SuccessResponse[BrandDiscoveryData]:
    data = await discover_brand_dna(payload.website_url)
    return SuccessResponse(data=data)
