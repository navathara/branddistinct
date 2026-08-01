"""
evaluation.py

Content Evaluation endpoint — POST /api/evaluate.

Matches Endpoint 2 in 08_api_contracts.md. Stays thin per the
developer handbook: it only validates the request shape (via
EvaluateRequest) and delegates all work to the Evaluation Engine
service. All failure modes are raised as typed exceptions from
core.exceptions and handled globally (see main.py's exception
handlers), so this file never needs its own try/except blocks.
"""

from fastapi import APIRouter

from models.evaluation import EvaluateRequest, EvaluationData
from models.response import SuccessResponse
from services.evaluation_service import evaluate_content

router = APIRouter()


@router.post("/evaluate", response_model=SuccessResponse[EvaluationData])
async def evaluate(payload: EvaluateRequest) -> SuccessResponse[EvaluationData]:
    data = await evaluate_content(payload.brand_dna, payload.content_type, payload.content)
    return SuccessResponse(data=data)
