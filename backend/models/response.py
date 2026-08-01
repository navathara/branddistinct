"""
response.py

Standard API response envelope schemas, as defined in
08_api_contracts.md ("Standard Response Format").

Every endpoint in the system returns one of these two shapes:

    SuccessResponse[T]:
        {"success": true, "data": {...}, "message": "..."}

    ErrorResponse:
        {"success": false, "error": {"code": "...", "message": "..."}}

Defined once here so every future endpoint (Brand Discovery,
Evaluate) reuses the same envelope instead of redefining it,
keeping frontend/backend contracts consistent per the stability
policy in 08_api_contracts.md.
"""

from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ErrorDetail(BaseModel):
    code: str
    message: str


class SuccessResponse(BaseModel, Generic[T]):
    success: bool = True
    data: T
    message: str = "Operation completed successfully."


class ErrorResponse(BaseModel):
    success: bool = False
    error: ErrorDetail
