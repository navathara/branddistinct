"""
evidence.py

Deterministic assembly of the Evidence Matrix, per
03_evaluation_pipeline.yaml step_6 (Evidence Matrix Generation) and
04_bdsf_methodology.yaml's `evidence_matrix.generated_for_each_dimension`
(matched_attributes, conflicting_attributes, supporting_examples).

No LLM calls happen here — this is a pure structural transform. The
AI already produced the evidence per canonical dimension as part of
the content-evaluation response (models.evaluation.
CanonicalDimensionResult.evidence); this module is only responsible
for organizing those six blocks into the matrix keyed by dimension
name, exactly as the API contract's `evidence_matrix` field expects.
"""

from models.evaluation import ContentEvaluationResult, EvidenceMatrixEntry


def build_evidence_matrix(evaluation: ContentEvaluationResult) -> dict[str, EvidenceMatrixEntry]:
    """
    Builds the Evidence Matrix from a validated ContentEvaluationResult,
    one entry per canonical Brand DNA dimension (01_brand_dna.yaml).
    """
    return {
        "identity": EvidenceMatrixEntry(**evaluation.identity.evidence.model_dump()),
        "personality": EvidenceMatrixEntry(**evaluation.personality.evidence.model_dump()),
        "communication": EvidenceMatrixEntry(**evaluation.communication.evidence.model_dump()),
        "audience": EvidenceMatrixEntry(**evaluation.audience.evidence.model_dump()),
        "visual_identity": EvidenceMatrixEntry(**evaluation.visual_identity.evidence.model_dump()),
        "values": EvidenceMatrixEntry(**evaluation.values.evidence.model_dump()),
    }
