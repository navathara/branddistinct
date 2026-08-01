interface BrandMarkProps {
  className?: string;
}

/**
 * The hexagon traces the six canonical Brand DNA dimensions
 * (identity, personality, communication, audience, visual identity,
 * values — see 01_brand_dna.yaml) as a single closed shape: one brand,
 * one signature. Used at small scale in the navbar and at large scale
 * as the hero's signature graphic.
 */
export function BrandMark({ className }: BrandMarkProps) {
  return (
    <svg
      viewBox="0 0 32 32"
      className={className}
      role="img"
      aria-label="BrandDistinct AI"
    >
      <polygon
        points="16,3 27,9.5 27,22.5 16,29 5,22.5 5,9.5"
        fill="none"
        stroke="var(--color-ink-900)"
        strokeWidth="1.6"
      />
      <polygon
        points="16,9 21.5,12.5 21.5,19.5 16,23 10.5,19.5 10.5,12.5"
        fill="var(--color-signal-600)"
      />
    </svg>
  );
}
