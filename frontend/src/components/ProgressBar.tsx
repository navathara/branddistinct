import { toneForPercent, TONE_BAR_CLASS } from "@/utils/scoreTone";

interface ProgressBarProps {
  /** 0–100. Values outside this range are clamped. */
  percent: number;
  /** Accessible label, e.g. "Overall score, 82 out of 100". */
  label: string;
}

export function ProgressBar({ percent, label }: ProgressBarProps) {
  const clamped = Math.min(100, Math.max(0, percent));
  const tone = toneForPercent(clamped);

  return (
    <div
      role="progressbar"
      aria-label={label}
      aria-valuenow={Math.round(clamped)}
      aria-valuemin={0}
      aria-valuemax={100}
      className="h-2 w-full overflow-hidden rounded-full bg-surface-2"
    >
      <div
        className={`h-full rounded-full transition-[width] ${TONE_BAR_CLASS[tone]}`}
        style={{ width: `${clamped}%` }}
      />
    </div>
  );
}
