import { Link } from "react-router-dom";

export function NotFound() {
  return (
    <div className="mx-auto flex max-w-6xl flex-col items-start gap-4 px-6 py-24">
      <p className="font-mono text-sm text-signal-600">404</p>
      <h1 className="font-display text-3xl font-semibold text-ink-900">
        This page isn't built yet.
      </h1>
      <p className="max-w-md text-ink-600">
        Nothing lives at this address yet. Head back to the home page and
        pick up from there.
      </p>
      <Link
        to="/"
        className="rounded-card bg-ink-900 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-ink-600"
      >
        Back to home
      </Link>
    </div>
  );
}
