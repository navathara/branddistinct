"""
router.py

Aggregates all API route modules into a single router that main.py
mounts under the configured API prefix (/api).

Adding a new endpoint group later means: create a new module under
api/routes/, then register it here. main.py never needs to change.
"""

from fastapi import APIRouter

from api.routes import (
    brand_discovery,
    evaluation,
    health,
    rewrite,
)

api_router = APIRouter()

api_router.include_router(health.router, tags=["Health"])
api_router.include_router(brand_discovery.router, tags=["Brand Discovery"])
api_router.include_router(evaluation.router, tags=["Evaluation"])
api_router.include_router(rewrite.router, tags=["Rewrite"])
