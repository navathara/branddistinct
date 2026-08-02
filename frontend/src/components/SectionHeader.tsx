interface Props { eyebrow?: string; title: string; description?: string; }
export function SectionHeader({ eyebrow, title, description }: Props) {
 return <div>{eyebrow && <p className="font-mono text-xs uppercase tracking-[.14em] text-signal-600">{eyebrow}</p>}<h2 className="mt-2 font-display text-2xl font-semibold text-ink-900">{title}</h2>{description && <p className="mt-2 max-w-2xl text-sm leading-relaxed text-ink-600">{description}</p>}</div>;
}