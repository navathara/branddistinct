import { ScoreCard } from "@/components/ScoreCard";
import type { BdsfDimensionScores } from "@/types/evaluation";

interface DimensionScoresPanelProps {
  scores: BdsfDimensionScores;
}

/** Labels and weights straight from 02_bdsf.yaml's `dimensions` block. */
const DIMENSION_META: {
  key: keyof BdsfDimensionScores;
  label: string;
  weight: number;
}[] = [
  { key: "identity_alignment", label: "Identity Alignment", weight: 30 },
  { key: "distinctiveness", label: "Distinctiveness", weight: 25 },
  { key: "consistency", label: "Consistency", weight: 20 },
  { key: "audience_resonance", label: "Audience Resonance", weight: 15 },
  { key: "values_alignment", label: "Values Alignment", weight: 10 },
];

export function DimensionScoresPanel({ scores }: DimensionScoresPanelProps) {
  return (
    <section>
      <h2 className="font-display text-lg font-semibold text-ink-900">
        BDSF Dimension Scores
      </h2>
      <p className="mt-1 text-sm text-ink-600">
        Each dimension is weighted differently in the overall score.
      </p>

      <div className="mt-4 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {DIMENSION_META.map(({ key, label, weight }) => (
          <ScoreCard
            key={key}
            label={label}
            caption={`Weight: ${weight}%`}
            value={scores[key]}
          />
        ))}
      </div>
    </section>
  );
}
