import { useBrand } from "@/context/BrandContext";
import { useNavigate } from "react-router-dom";
import { BrandDiscoveryForm } from "@/components/BrandDiscoveryForm";
import { BrandDnaResult } from "@/components/BrandDnaResult";
import { useApi } from "@/hooks/useApi";
import { discoverBrand } from "@/services/brandService";

export function Discover() {
  const { status, data, error, run } = useApi(discoverBrand);
  const { setBrand } = useBrand();
  const navigate = useNavigate();

  return (
    <div className="mx-auto max-w-6xl px-6 py-16">
      <p className="font-mono text-xs uppercase tracking-[0.14em] text-signal-600">
        Step 1 of 2
      </p>

      <h1 className="mt-2 font-display text-3xl font-semibold text-ink-900">
        Discover your Brand DNA
      </h1>

      <p className="mt-3 max-w-xl text-ink-600">
        Enter a website URL. We'll extract a structured Brand DNA profile
        across the six canonical dimensions — you'll be able to review it
        before anything gets scored.
      </p>

      <div className="mt-8">
        <BrandDiscoveryForm
          isLoading={status === "loading"}
          onSubmit={run}
        />
      </div>

      {status === "loading" && (
        <div
          role="status"
          aria-live="polite"
          className="mt-10 flex items-center gap-3 rounded-card border border-surface-2 bg-surface-1 px-5 py-4"
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

      {status === "error" && (
        <div
          role="alert"
          className="mt-10 rounded-card border border-warn-600/30 bg-surface-1 px-5 py-4"
        >
          <p className="font-mono text-xs uppercase tracking-[0.06em] text-warn-600">
            {error.code}
          </p>

          <p className="mt-1 text-sm text-ink-900">
            {error.message}
          </p>
        </div>
      )}

      {status === "success" && data && (
        <div className="mt-10 space-y-6">
          <BrandDnaResult result={data} />

          <div className="flex justify-end">
            <button
              type="button"
              onClick={() => {
                setBrand(data);
                navigate("/evaluate");
              }}
              className="rounded-xl bg-signal-600 px-6 py-3 font-medium text-white transition hover:bg-signal-500"
            >
              Continue to Evaluation →
            </button>
          </div>
        </div>
      )}
    </div>
  );
}