import { useState, type FormEvent } from "react";

interface EvaluationFormProps {
  isLoading: boolean;
  onSubmit: (content: string) => void;
}

export function EvaluationForm({ isLoading, onSubmit }: EvaluationFormProps) {
  const [content, setContent] = useState("");
  const [validationError, setValidationError] = useState<string | null>(null);

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const trimmed = content.trim();
    if (!trimmed) {
      setValidationError("Paste the content you want to evaluate.");
      return;
    }

    setValidationError(null);
    onSubmit(trimmed);
  }

  return (
    <form onSubmit={handleSubmit} noValidate className="flex flex-col gap-3">
      <div>
        <label htmlFor="evaluation_content" className="sr-only">
          Marketing content
        </label>
        <textarea
          id="evaluation_content"
          name="evaluation_content"
          rows={8}
          placeholder="Paste an ad, caption, product description, or email..."
          value={content}
          onChange={(event) => {
            setContent(event.target.value);
            if (validationError) setValidationError(null);
          }}
          disabled={isLoading}
          aria-invalid={validationError ? "true" : "false"}
          aria-describedby={validationError ? "evaluation_content_error" : undefined}
          className="w-full resize-y rounded-card border border-surface-2 bg-surface-1 px-4 py-3 text-sm leading-relaxed text-ink-900 placeholder:text-ink-400 disabled:opacity-60"
        />
        {validationError && (
          <p id="evaluation_content_error" role="alert" className="mt-2 text-sm text-warn-600">
            {validationError}
          </p>
        )}
      </div>

      <button
        type="submit"
        disabled={isLoading}
        className="self-start rounded-card bg-signal-600 px-5 py-3 text-sm font-medium text-white transition-colors hover:bg-signal-500 disabled:cursor-not-allowed disabled:opacity-60"
      >
        {isLoading ? "Evaluating…" : "Evaluate Content"}
      </button>
    </form>
  );
}
