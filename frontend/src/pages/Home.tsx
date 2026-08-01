import { Link } from "react-router-dom";
import { DimensionSignature } from "@/components/DimensionSignature";

const WORKFLOW = [
  {
    step: "Discover",
    description:
      "Point to a website. We extract a structured Brand DNA profile across six dimensions.",
  },
  {
    step: "Review",
    description:
      "Verify and adjust the Brand DNA before anything is scored — the record of truth stays human-approved.",
  },
  {
    step: "Evaluate",
    description:
      "Submit text or images. Each dimension is scored against the Brand DNA using the BDSF.",
  },
  {
    step: "Improve",
    description:
      "Get an evidence-backed score, plus quick fixes and strategic recommendations.",
  },
];

export function Home() {
  return (
    <div>
      {/* Hero */}
      <section className="grid-surface border-b border-surface-2">
        <div className="mx-auto grid max-w-6xl grid-cols-1 items-center gap-12 px-6 py-20 md:grid-cols-2 md:py-28">
          <div>
            <p className="font-mono text-xs uppercase tracking-[0.14em] text-signal-600">
              Brand Distinctiveness Scoring Framework
            </p>
            <h1 className="mt-4 font-display text-4xl font-semibold leading-[1.05] tracking-tight text-ink-900 sm:text-5xl">
              BrandDistinct AI
            </h1>
            <p className="mt-5 max-w-lg text-lg leading-relaxed text-ink-600">
              Measure how closely AI-generated text and images hold onto a
              brand's identity. Every score comes with the evidence behind
              it, so you can see exactly why content does or doesn't fit.
            </p>
            <div className="mt-8 flex items-center gap-4">
              <Link
                to="/discover"
                className="rounded-card bg-signal-600 px-5 py-3 text-sm font-medium text-white transition-colors hover:bg-signal-500"
              >
                Start Analysis
              </Link>
              <span className="text-sm text-ink-400">
                No signup — start with a website URL.
              </span>
            </div>
          </div>

          <div className="flex justify-center">
            <DimensionSignature className="w-full max-w-sm" />
          </div>
        </div>
      </section>

      {/* Workflow */}
      <section className="mx-auto max-w-6xl px-6 py-20">
        <h2 className="font-display text-2xl font-semibold text-ink-900">
          How it works
        </h2>
        <p className="mt-2 max-w-xl text-ink-600">
          One pipeline, four stages — from a raw website to an explainable
          score.
        </p>

        <ol className="mt-10 grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-4">
          {WORKFLOW.map((item, index) => (
            <li key={item.step} className="relative pl-0">
              <div className="flex items-center gap-3">
                <span className="font-mono text-xs text-ink-400">
                  {String(index + 1).padStart(2, "0")}
                </span>
                <div className="h-px flex-1 bg-surface-2" aria-hidden="true" />
              </div>
              <h3 className="mt-3 font-display text-lg font-semibold text-ink-900">
                {item.step}
              </h3>
              <p className="mt-2 text-sm leading-relaxed text-ink-600">
                {item.description}
              </p>
            </li>
          ))}
        </ol>
      </section>
    </div>
  );
}
