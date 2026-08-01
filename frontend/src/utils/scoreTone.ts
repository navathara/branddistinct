/**
 * Maps a score to one of the existing design tokens (`good-600` /
 * `warn-600` — there is no third "critical" tone in the design system, so
 * low scores also use `warn-600`). Shared by every Results Dashboard
 * component so thresholds stay consistent across the whole dashboard.
 */
export type ScoreTone = "good" | "warn";

const GOOD_THRESHOLD = 70;

export function toneForPercent(percent: number): ScoreTone {
  return percent >= GOOD_THRESHOLD ? "good" : "warn";
}

export function toneForScore(score: number, max = 100): ScoreTone {
  return toneForPercent((score / max) * 100);
}

export const TONE_TEXT_CLASS: Record<ScoreTone, string> = {
  good: "text-good-600",
  warn: "text-warn-600",
};

export const TONE_BAR_CLASS: Record<ScoreTone, string> = {
  good: "bg-good-600",
  warn: "bg-warn-600",
};
