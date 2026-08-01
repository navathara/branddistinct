from fastapi import APIRouter

from models.evaluation import RewriteRequest, RewriteData
from services.rewrite_service import rewrite_content

router = APIRouter(tags=["Rewrite"])


@router.post("/rewrite")
async def rewrite(request: RewriteRequest):

    result = await rewrite_content(
        request.brand_dna,
        request.content,
    )

    return {
        "success": True,
        "data": RewriteData(
            rewritten_content=result["rewritten_content"],
            improvement_summary=result["improvement_summary"],
        ),
        "message": "Rewrite generated successfully.",
    }
