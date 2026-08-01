import { useState } from "react";
import { rewriteContent } from "@/services/rewriteService";
import { BrandDiscoveryForm } from "@/components/BrandDiscoveryForm";
import { BrandDnaResult } from "@/components/BrandDnaResult";
import { EvaluationForm } from "@/components/EvaluationForm";
import { ResultsDashboard } from "@/components/ResultsDashboard";
import { useApi } from "@/hooks/useApi";
import { discoverBrand } from "@/services/brandService";
import { evaluateContent } from "@/services/evaluationService";

export function Evaluate() {
  const discovery = useApi(discoverBrand);
  const evaluation = useApi(evaluateContent);
  const rewrite = useApi(rewriteContent);
  const [originalContent, setOriginalContent] = useState("");
  const brand = discovery.status === "success" ? discovery.data : null;

  function handleEvaluate(content: string) {
    if (!brand) return;

    setOriginalContent(content);

    evaluation.run({
      brand_id: brand.brand_id,
      content_type: "text",
      content,
      brand_dna: brand.brand_dna,
    });
  }

  function handleRewrite(content: string) {
    if (!brand) return;

    rewrite.run({
      brand_dna: brand.brand_dna,
      content,
    });
  }


  function handleUseDifferentWebsite() {
    discovery.reset();
    evaluation.reset();
    rewrite.reset();
    setOriginalContent("");
  }

  return (
    <div className="mx-auto max-w-6xl px-6 py-16">
      <p className="font-mono text-xs uppercase tracking-[0.14em] text-signal-600">
        Evaluate Content
      </p>
      <h1 className="mt-2 font-display text-3xl font-semibold text-ink-900">
        Check content against a Brand DNA
      </h1>
      <p className="mt-3 max-w-xl text-ink-600">
        Provide the Brand DNA to evaluate against, then paste the content
        you want scored.
      </p>

      {/* Step 1 — Brand DNA, via the existing Brand Discovery flow */}
      {!brand && (
        <section className="mt-10">
          <h2 className="font-display text-lg font-semibold text-ink-900">
            1. Provide the Brand DNA
          </h2>
          <p className="mt-1 text-sm text-ink-600">
            Enter the website for the brand you want to evaluate against.
          </p>

          <div className="mt-5">
            <BrandDiscoveryForm
              isLoading={discovery.status === "loading"}
              onSubmit={discovery.run}
            />
          </div>

          {discovery.status === "loading" && (
            <div
              role="status"
              aria-live="polite"
              className="mt-6 flex items-center gap-3 rounded-card border border-surface-2 bg-surface-1 px-5 py-4"
            >
              <span
                className="h-4 w-4 animate-spin rounded-full border-2 border-signal-600 border-t-transparent"
                aria-hidden="true"
              />
              <p className="text-sm text-ink-600">
                Reading the site and extracting Brand DNA — this can take a moment.
              </p>
            </div>
          )}

          {discovery.status === "error" && (
            <div
              role="alert"
              className="mt-6 rounded-card border border-warn-600/30 bg-surface-1 px-5 py-4"
            >
              <p className="font-mono text-xs uppercase tracking-[0.06em] text-warn-600">
                {discovery.error.code}
              </p>
              <p className="mt-1 text-sm text-ink-900">{discovery.error.message}</p>
            </div>
          )}
        </section>
      )}

      {/* Step 2 — Content submission, once a Brand DNA is available */}
      {brand && (
        <section className="mt-10">
          <div className="flex flex-wrap items-center justify-between gap-3 rounded-card border border-surface-2 bg-surface-1 px-5 py-4">
            <p className="text-sm text-ink-900">
              Evaluating against{" "}
              <span className="font-semibold">{brand.brand_name}</span>
              <span className="ml-2 font-mono text-xs text-ink-400">
                {Math.round(brand.extraction_confidence * 100)}% extraction confidence
              </span>
            </p>
            <button
              type="button"
              onClick={handleUseDifferentWebsite}
              className="text-sm font-medium text-signal-600 hover:text-signal-500"
            >
              Use a different website
            </button>
          </div>

          <details className="mt-3 rounded-card border border-surface-2 bg-surface-1 px-5 py-4">
            <summary className="cursor-pointer text-sm font-medium text-ink-900">
              View extracted Brand DNA
            </summary>
            <div className="mt-5">
              <BrandDnaResult result={brand} />
            </div>
          </details>

          <h2 className="mt-8 font-display text-lg font-semibold text-ink-900">
            2. Paste content to evaluate
          </h2>

          <div className="mt-5">
            <EvaluationForm
              isLoading={evaluation.status === "loading"}
              onSubmit={handleEvaluate}
            />
          </div>

          {evaluation.status === "loading" && (
            <div
              role="status"
              aria-live="polite"
              className="mt-6 flex items-center gap-3 rounded-card border border-surface-2 bg-surface-1 px-5 py-4"
            >
              <span
                className="h-4 w-4 animate-spin rounded-full border-2 border-signal-600 border-t-transparent"
                aria-hidden="true"
              />
              <p className="text-sm text-ink-600">
                Scoring content against the Brand DNA…
              </p>
            </div>
          )}

          {evaluation.status === "success" && evaluation.data && (
            <div className="mt-10">
              <h2 className="font-display text-lg font-semibold text-ink-900">
                Results
              </h2>

              <div className="mt-5">
                <ResultsDashboard result={evaluation.data} />
              </div>

              {/* Rewrite Button */}
              <div className="mt-6">
                <button
                  type="button"
                  onClick={() => handleRewrite(originalContent)}
                  disabled={rewrite.status === "loading"}
                  className="rounded-card bg-signal-600 px-5 py-3 text-sm font-medium text-white transition-colors hover:bg-signal-500 disabled:cursor-not-allowed disabled:opacity-60"
                >
                  {rewrite.status === "loading"
                    ? "Rewriting..."
                    : "✨ Rewrite Content"}
                </button>
              </div>

              {/* Rewrite Error */}
              {rewrite.status === "error" && (
                <div
                  role="alert"
                  className="mt-6 rounded-card border border-warn-600/30 bg-surface-1 px-5 py-4"
                >
                  <p className="font-mono text-xs uppercase tracking-[0.06em] text-warn-600">
                    {rewrite.error.code}
                  </p>

                  <p className="mt-1 text-sm text-ink-900">
                    {rewrite.error.message}
                  </p>
                </div>
              )}

              {/* Rewrite Result */}
              {rewrite.status === "success" && rewrite.data && (
                <div className="mt-8 rounded-card border border-surface-2 bg-surface-1 p-6">
                  <h3 className="font-display text-lg font-semibold text-ink-900">
                    ✨ AI Rewritten Content
                  </h3>

                  <p className="mt-4 whitespace-pre-wrap text-sm leading-relaxed text-ink-700">
                    {rewrite.data.rewritten_content}
                  </p>

                  {rewrite.data.improvement_summary.length > 0 && (
                    <>
                      <h4 className="mt-6 font-semibold text-ink-900">
                        Improvements Made
                      </h4>

                      <ul className="mt-2 list-disc pl-6 text-sm text-ink-700">
                        {rewrite.data.improvement_summary.map((item, index) => (
                          <li key={index}>{item}</li>
                        ))}
                      </ul>
                    </>
                  )}
                </div>
              )}
            </div>
          )}
        </section>
      )}
    </div>
  );
}
