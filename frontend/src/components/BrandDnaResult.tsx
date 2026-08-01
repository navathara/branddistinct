import { BrandDnaDimensionCard } from "@/components/BrandDnaDimensionCard";
import {
  BRAND_DNA_DIMENSION_KEYS,
  BRAND_DNA_DIMENSION_LABELS,
  type DiscoverBrandResult,
} from "@/types/brand";

interface BrandDnaResultProps {
  result: DiscoverBrandResult;
}

function confidenceTone(confidence: number): string {
  if (confidence >= 0.75) return "text-good-600";
  if (confidence >= 0.5) return "text-warn-600";
  return "text-warn-600";
}

export function BrandDnaResult({ result }: BrandDnaResultProps) {
  const confidencePercent = Math.round(result.extraction_confidence * 100);

  return (
    <div>
      <div className="flex flex-wrap items-end justify-between gap-4 border-b border-surface-2 pb-6">
        <div>
          <p className="font-mono text-xs uppercase tracking-[0.14em] text-signal-600">
            Brand DNA extracted
          </p>
          <h2 className="mt-2 font-display text-2xl font-semibold text-ink-900">
            {result.brand_name}
          </h2>
        </div>

        <div className="text-right">
          <p className="font-mono text-xs uppercase tracking-[0.06em] text-ink-400">
            Extraction confidence
          </p>
          <p className={`font-display text-2xl font-semibold ${confidenceTone(result.extraction_confidence)}`}>
            {confidencePercent}%
          </p>
        </div>
      </div>

      <div className="mt-6 grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
        {BRAND_DNA_DIMENSION_KEYS.map((key) => (
          <BrandDnaDimensionCard
            key={key}
            label={BRAND_DNA_DIMENSION_LABELS[key]}
            dimension={result.brand_dna[key] ?? {}}
          />
        ))}
      </div>
    </div>
  );
}
