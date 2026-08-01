interface EvidenceMatrixPanelProps {
  evidenceMatrix: Record<string, unknown>;
}

function formatKey(key: string): string {
  return key
    .split("_")
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
    .join(" ");
}

/**
 * Renders an arbitrary evidence value. `evidence_matrix` isn't tied to a
 * fixed shape in the response type (04_bdsf_methodology.yaml describes
 * `matched_attributes` / `conflicting_attributes` / `supporting_examples`
 * per dimension, but the exact nesting is up to the backend), so this
 * walks whatever comes back rather than assuming a schema.
 */
function EvidenceValue({ value }: { value: unknown }) {
  if (value === null || value === undefined) {
    return <span className="text-ink-400">—</span>;
  }

  if (Array.isArray(value)) {
    if (value.length === 0) return <span className="text-ink-400">None</span>;
    return (
      <ul className="list-disc space-y-1 pl-4">
        {value.map((item, index) => (
          <li key={index} className="text-sm leading-relaxed text-ink-600">
            {typeof item === "object" ? <EvidenceValue value={item} /> : String(item)}
          </li>
        ))}
      </ul>
    );
  }

  if (typeof value === "object") {
    const entries = Object.entries(value as Record<string, unknown>);
    if (entries.length === 0) return <span className="text-ink-400">None</span>;
    return (
      <dl className="space-y-2">
        {entries.map(([key, nested]) => (
          <div key={key}>
            <dt className="font-mono text-xs uppercase tracking-[0.06em] text-ink-400">
              {formatKey(key)}
            </dt>
            <dd className="mt-1">
              <EvidenceValue value={nested} />
            </dd>
          </div>
        ))}
      </dl>
    );
  }

  return <span className="text-sm leading-relaxed text-ink-600">{String(value)}</span>;
}

export function EvidenceMatrixPanel({ evidenceMatrix }: EvidenceMatrixPanelProps) {
  const entries = Object.entries(evidenceMatrix);

  return (
    <section>
      <h2 className="font-display text-lg font-semibold text-ink-900">Evidence Matrix</h2>
      <p className="mt-1 text-sm text-ink-600">
        Matched and conflicting attributes behind each dimension's score.
      </p>

      {entries.length === 0 ? (
        <div className="mt-4 rounded-card border border-surface-2 bg-surface-1 p-5">
          <p className="text-sm text-ink-400">No evidence was returned for this evaluation.</p>
        </div>
      ) : (
        <div className="mt-4 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {entries.map(([key, value]) => (
            <div key={key} className="rounded-card border border-surface-2 bg-surface-1 p-5">
              <h3 className="font-display text-base font-semibold text-ink-900">
                {formatKey(key)}
              </h3>
              <div className="mt-3">
                <EvidenceValue value={value} />
              </div>
            </div>
          ))}
        </div>
      )}
    </section>
  );
}
