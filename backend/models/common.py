"""
common.py

Small, shared Pydantic schemas that don't belong to any single
future domain module (brand DNA, evaluation, etc.).

Currently only holds the health check response. Kept separate from
response.py so this file can stay tiny and dependency-free.
"""

from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
