import { ProgressBar } from "@/components/ProgressBar";
import { toneForPercent, TONE_TEXT_CLASS } from "@/utils/scoreTone";

interface ScoreCardProps {
  label: string;
  /** Raw value to display, e.g. 82, 0.93, or 8. */
  value: number;
  /** The value's maximum on its own scale (default 100). Used only to size the bar. */
  max?: number;
  /** Text shown next to the displayed value, e.g. "/100", "%", " pts". */
  suffix?: string;
  /** Optional caption under the label, e.g. a BDSF dimension's weight. */
  caption?: string;
  /** When true, inverts color meaning (a higher value is worse — e.g. a penalty). */
  invertTone?: boolean;
}

export function ScoreCard({
  label,
  value,
  max = 100,
  suffix = "/100",
  caption,
  invertTone = false,
}: ScoreCardProps) {
  const percent = max > 0 ? Math.min(100, Math.max(0, (value / max) * 100)) : 0;
  const tone = toneForPercent(invertTone ? 100 - percent : percent);
  const displayValue = Number.isInteger(value) ? value : value.toFixed(1);

  return (
    <div className="rounded-card border border-surface-2 bg-surface-1 p-5">
      <p className="font-mono text-xs uppercase tracking-[0.06em] text-ink-400">{label}</p>
      {caption && <p className="mt-0.5 text-xs text-ink-400">{caption}</p>}

      <p className={`mt-2 font-display text-3xl font-semibold ${TONE_TEXT_CLASS[tone]}`}>
        {displayValue}
        <span className="text-base font-normal text-ink-400">{suffix}</span>
      </p>

      <div className="mt-4">
        <ProgressBar percent={percent} label={`${label}, ${displayValue}${suffix}`} />
      </div>
    </div>
  );
}
