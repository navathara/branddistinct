import { Link } from "react-router-dom";
import { BrandMark } from "@/components/BrandMark";

export function Navbar() {
  return (
    <header className="border-b border-surface-2 bg-surface-1/80 backdrop-blur">
      <div className="mx-auto flex h-16 max-w-6xl items-center justify-between px-6">
        <Link to="/" className="flex items-center gap-2.5">
          <BrandMark className="h-7 w-7" />
          <span className="font-display text-[1.05rem] font-semibold tracking-tight text-ink-900">
            BrandDistinct AI
          </span>
        </Link>

        <Link
          to="/discover"
          className="rounded-card bg-signal-600 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-signal-500"
        >
          Start Analysis
        </Link>
      </div>
    </header>
  );
}
