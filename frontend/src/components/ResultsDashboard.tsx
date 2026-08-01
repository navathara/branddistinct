import { DimensionScoresPanel } from "@/components/DimensionScoresPanel";
import { EvidenceMatrixPanel } from "@/components/EvidenceMatrixPanel";
import { RecommendationsPanel } from "@/components/RecommendationsPanel";
import { ScoreCard } from "@/components/ScoreCard";
import type { EvaluateContentResult } from "@/types/evaluation";

interface ResultsDashboardProps {
  result: EvaluateContentResult;
}

/**
 * Full, explainable breakdown of a single evaluation response — overall
 * score, the five BDSF dimension scores, genericness penalty, evaluation
 * confidence, evidence matrix, and recommendations.
 *
 * Pure presentation: it takes the existing `EvaluateContentResult` as-is
 * and renders it. No API calls, no page, no route — this is the
 * component future pages (e.g. a dedicated results route) will mount.
 */
export function ResultsDashboard({ result }: ResultsDashboardProps) {
  return (
    <div className="flex flex-col gap-10">
      <section>
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
          <ScoreCard label="Overall Score" value={result.overall_score} max={100} />
          <ScoreCard
            label="Evaluation Confidence"
            value={Math.round(result.evaluation_confidence * 100)}
            max={100}
            suffix="%"
          />
          <ScoreCard
            label="Genericness Penalty"
            value={result.genericness_penalty}
            max={20}
            suffix=" pts"
            invertTone
          />
        </div>
      </section>

      <DimensionScoresPanel scores={result.dimension_scores} />

      <EvidenceMatrixPanel evidenceMatrix={result.evidence_matrix} />

      <RecommendationsPanel recommendations={result.recommendations} />
    </div>
  );
}
