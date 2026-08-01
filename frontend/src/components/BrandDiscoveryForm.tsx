import { useState, type FormEvent } from "react";
import { validateWebsiteUrl } from "@/utils/validateWebsiteUrl";

interface BrandDiscoveryFormProps {
  isLoading: boolean;
  onSubmit: (websiteUrl: string) => void;
}

export function BrandDiscoveryForm({ isLoading, onSubmit }: BrandDiscoveryFormProps) {
  const [websiteUrl, setWebsiteUrl] = useState("");
  const [validationError, setValidationError] = useState<string | null>(null);

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const error = validateWebsiteUrl(websiteUrl);
    if (error) {
      setValidationError(error);
      return;
    }

    setValidationError(null);
    onSubmit(websiteUrl.trim());
  }

  return (
    <form onSubmit={handleSubmit} noValidate className="flex flex-col gap-2 sm:flex-row sm:items-start sm:gap-3">
      <div className="flex-1">
        <label htmlFor="website_url" className="sr-only">
          Website URL
        </label>
        <input
          id="website_url"
          name="website_url"
          type="text"
          inputMode="url"
          autoComplete="url"
          placeholder="https://yourcompany.com"
          value={websiteUrl}
          onChange={(event) => {
            setWebsiteUrl(event.target.value);
            if (validationError) setValidationError(null);
          }}
          disabled={isLoading}
          aria-invalid={validationError ? "true" : "false"}
          aria-describedby={validationError ? "website_url_error" : undefined}
          className="w-full rounded-card border border-surface-2 bg-surface-1 px-4 py-3 text-sm text-ink-900 placeholder:text-ink-400 disabled:opacity-60"
        />
        {validationError && (
          <p id="website_url_error" role="alert" className="mt-2 text-sm text-warn-600">
            {validationError}
          </p>
        )}
      </div>

      <button
        type="submit"
        disabled={isLoading}
        className="rounded-card bg-signal-600 px-5 py-3 text-sm font-medium text-white transition-colors hover:bg-signal-500 disabled:cursor-not-allowed disabled:opacity-60"
      >
        {isLoading ? "Analyzing…" : "Discover Brand DNA"}
      </button>
    </form>
  );
}
