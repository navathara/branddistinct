"""
health.py

Health check endpoint — GET /api/health.

Matches Endpoint 3 in 08_api_contracts.md exactly:

    {
      "status": "healthy"
    }

Used to verify backend availability (e.g. by the frontend, a
deployment platform, or during the live demo to prove the service
is up before evaluation runs). Contains no business logic and will
never depend on services/ or core/.
"""

from fastapi import APIRouter

from models.common import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    return HealthResponse(status="healthy")
