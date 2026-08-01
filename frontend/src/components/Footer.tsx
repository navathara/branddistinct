export function Footer() {
  return (
    <footer className="border-t border-surface-2">
      <div className="mx-auto flex max-w-6xl flex-col gap-2 px-6 py-8 text-sm text-ink-400 sm:flex-row sm:items-center sm:justify-between">
        <p>© {new Date().getFullYear()} BrandDistinct AI. Built for the hackathon.</p>
        <p className="font-mono text-xs">Brand Distinctiveness Scoring Framework (BDSF)</p>
      </div>
    </footer>
  );
}
