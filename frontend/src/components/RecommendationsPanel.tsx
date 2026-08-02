import type { EvaluationRecommendations } from "@/types/evaluation";

interface RecommendationsPanelProps {
  recommendations: EvaluationRecommendations;
}

function RecommendationList({ items, empty }: { items: string[]; empty: string }) {
  if (items.length === 0) {
    return <p className="mt-3 text-sm text-ink-400">{empty}</p>;
  }
  return (
    <ul className="mt-3 space-y-2">
      {items.map((item, index) => (
        <li key={index} className="flex gap-2 text-sm leading-relaxed text-ink-600">
          <span className="text-signal-600" aria-hidden="true">
            →
          </span>
          <span>{item}</span>
        </li>
      ))}
    </ul>
  );
}

export function RecommendationsPanel({ recommendations }: RecommendationsPanelProps) {
  return (
    <section>
      <h2 className="font-display text-lg font-semibold text-ink-900">Recommendations</h2>
      <p className="mt-1 text-sm text-ink-600">
        Immediate fixes and longer-term improvements for brand alignment.
      </p>

      <div className="mt-4 grid grid-cols-1 gap-4 sm:grid-cols-2">
        <div className="card-elevated rounded-xl border border-surface-2 bg-surface-1 p-5">
          <h3 className="font-display text-base font-semibold text-ink-900">Quick Fixes</h3>
          <RecommendationList
            items={recommendations.quick_fixes}
            empty="No quick fixes suggested."
          />
        </div>

        <div className="card-elevated rounded-xl border border-surface-2 bg-surface-1 p-5">
          <h3 className="font-display text-base font-semibold text-ink-900">
            Strategic Improvements
          </h3>
          <RecommendationList
            items={recommendations.strategic_improvements}
            empty="No strategic improvements suggested."
          />
        </div>
      </div>
    </section>
  );
}
