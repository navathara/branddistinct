/**
 * Evaluation domain types for POST /api/evaluate (08_api_contracts.md,
 * Endpoint 2).
 *
 * This page only submits text content (see 05_multimodal_evaluation.md —
 * image evaluation is a separate, not-yet-built flow), so `content_type`
 * is narrowed to "text" here rather than the full "text" | "image" the
 * contract allows.
 */

export interface EvaluateContentRequest {
  brand_id: string;
  content_type: "text";
  content: string;
}

/** BDSF dimension scores, keyed exactly as in 02_bdsf.yaml's `dimensions`. */
export interface BdsfDimensionScores {
  identity_alignment: number;
  distinctiveness: number;
  consistency: number;
  audience_resonance: number;
  values_alignment: number;
}

export interface EvaluationRecommendations {
  quick_fixes: string[];
  strategic_improvements: string[];
}

/** `data` shape of a successful POST /api/evaluate response. */
export interface EvaluateContentResult {
  overall_score: number;
  dimension_scores: BdsfDimensionScores;
  genericness_penalty: number;
  evaluation_confidence: number;
  evidence_matrix: Record<string, unknown>;
  recommendations: EvaluationRecommendations;
}
