import { apiPost } from "@/services/apiClient";
import type { EvaluateContentRequest, EvaluateContentResult } from "@/types/evaluation";

/**
 * POST /api/evaluate — see 08_api_contracts.md, Endpoint 2.
 * Evaluates text content against a previously discovered Brand DNA.
 */
export function evaluateContent(
  request: EvaluateContentRequest,
): Promise<EvaluateContentResult> {
  return apiPost<EvaluateContentResult, EvaluateContentRequest>("/evaluate", request);
}
