import type { BrandDnaDimension, BrandDnaFieldValue } from "@/types/brand";

interface BrandDnaDimensionCardProps {
  label: string;
  dimension: BrandDnaDimension;
}

/** Turns a snake_case field key into a readable label, e.g. "tone_of_voice" -> "Tone Of Voice". */
function formatFieldKey(key: string): string {
  return key
    .split("_")
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
    .join(" ");
}

function formatFieldValue(value: BrandDnaFieldValue): string | null {
  if (value === null || value === undefined) return null;
  if (Array.isArray(value)) {
    return value.length > 0 ? value.join(", ") : null;
  }
  if (typeof value === "boolean") return value ? "Yes" : "No";
  const text = String(value).trim();
  return text.length > 0 ? text : null;
}

export function BrandDnaDimensionCard({ label, dimension }: BrandDnaDimensionCardProps) {
  const entries = Object.entries(dimension)
    .map(([key, value]) => [key, formatFieldValue(value)] as const)
    .filter((entry): entry is [string, string] => entry[1] !== null);

  return (
    <div className="rounded-card border border-surface-2 bg-surface-1 p-5">
      <h3 className="font-display text-base font-semibold text-ink-900">{label}</h3>

      {entries.length === 0 ? (
        <p className="mt-3 text-sm text-ink-400">No data extracted for this dimension.</p>
      ) : (
        <dl className="mt-3 space-y-3">
          {entries.map(([key, value]) => (
            <div key={key}>
              <dt className="font-mono text-xs uppercase tracking-[0.06em] text-ink-400">
                {formatFieldKey(key)}
              </dt>
              <dd className="mt-1 text-sm leading-relaxed text-ink-600">{value}</dd>
            </div>
          ))}
        </dl>
      )}
    </div>
  );
}
