interface DimensionSignatureProps {
  className?: string;
}

const DIMENSIONS = [
  { label: "Identity", x: 100, y: 14 },
  { label: "Personality", x: 178, y: 58 },
  { label: "Communication", x: 178, y: 146 },
  { label: "Audience", x: 100, y: 190 },
  { label: "Visual Identity", x: 22, y: 146 },
  { label: "Values", x: 22, y: 58 },
];

const OUTER_HEX = "100,24 169.3,64 169.3,140 100,180 30.7,140 30.7,64";
const GRID_HEX_INNER = "100,55.7 148.9,80 148.9,124 100,148.3 51.1,124 51.1,80";
const SIGNATURE_SHAPE =
  "100,42 143.3,84 162.4,136 100,158 30.7,140 61,88";

const SPOKES = [
  [100, 100, 100, 24],
  [100, 100, 169.3, 64],
  [100, 100, 169.3, 140],
  [100, 100, 100, 180],
  [100, 100, 30.7, 140],
  [100, 100, 30.7, 64],
];

/**
 * Decorative hero graphic — one static example "signature," not a live
 * score. It illustrates the idea from 01_brand_dna.yaml (six canonical
 * dimensions) and 02_bdsf.yaml (a weighted shape rather than a single
 * number), without wiring to the evaluation API.
 */
export function DimensionSignature({ className }: DimensionSignatureProps) {
  return (
    <svg viewBox="0 0 200 210" className={className} role="presentation" aria-hidden="true">
      <polygon points={OUTER_HEX} fill="none" stroke="var(--color-surface-2)" strokeWidth="1" />
      <polygon points={GRID_HEX_INNER} fill="none" stroke="var(--color-surface-2)" strokeWidth="1" />
      {SPOKES.map(([x1, y1, x2, y2], i) => (
        <line
          key={i}
          x1={x1}
          y1={y1}
          x2={x2}
          y2={y2}
          stroke="var(--color-surface-2)"
          strokeWidth="1"
        />
      ))}
      <polygon
        points={SIGNATURE_SHAPE}
        fill="var(--color-signal-100)"
        stroke="var(--color-signal-600)"
        strokeWidth="2"
        strokeLinejoin="round"
      />
      {DIMENSIONS.map((d) => (
        <text
          key={d.label}
          x={d.x}
          y={d.y}
          textAnchor="middle"
          fontFamily="var(--font-mono)"
          fontSize="7.5"
          fill="var(--color-ink-600)"
        >
          {d.label}
        </text>
      ))}
    </svg>
  );
}
