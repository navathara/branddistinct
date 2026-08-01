import type { EvaluateContentResult } from "@/types/evaluation";

interface EvaluationSummaryProps {
  result: EvaluateContentResult;
}

function scoreTone(score: number): string {
  if (score >= 70) return "text-good-600";
  if (score >= 40) return "text-warn-600";
  return "text-warn-600";
}

/**
 * Deliberately minimal: overall score, evaluation confidence, and the
 * genericness penalty, plus a short success message. Dimension scores,
 * the evidence matrix, and recommendations exist on
 * `EvaluateContentResult` but are reserved for the Results Dashboard,
 * which is a separate, not-yet-built feature.
 */
export function EvaluationSummary({ result }: EvaluationSummaryProps) {
  const confidencePercent = Math.round(result.evaluation_confidence * 100);

  return (
    <div className="rounded-card border border-surface-2 bg-surface-1 p-6">
      <p className="font-mono text-xs uppercase tracking-[0.14em] text-signal-600">
        Evaluation complete
      </p>
      <p className="mt-2 text-sm text-ink-600">
        Your content has been scored against the brand's DNA. A full,
        evidence-backed breakdown is on the way in the results dashboard.
      </p>

      <div className="mt-6 grid grid-cols-1 gap-6 sm:grid-cols-3">
        <div>
          <p className="font-mono text-xs uppercase tracking-[0.06em] text-ink-400">
            Overall score
          </p>
          <p className={`mt-1 font-display text-3xl font-semibold ${scoreTone(result.overall_score)}`}>
            {result.overall_score}
            <span className="text-base font-normal text-ink-400">/100</span>
          </p>
        </div>

        <div>
          <p className="font-mono text-xs uppercase tracking-[0.06em] text-ink-400">
            Evaluation confidence
          </p>
          <p className="mt-1 font-display text-3xl font-semibold text-ink-900">
            {confidencePercent}%
          </p>
        </div>

        <div>
          <p className="font-mono text-xs uppercase tracking-[0.06em] text-ink-400">
            Genericness penalty
          </p>
          <p className="mt-1 font-display text-3xl font-semibold text-ink-900">
            −{result.genericness_penalty}
          </p>
        </div>
      </div>
    </div>
  );
}
