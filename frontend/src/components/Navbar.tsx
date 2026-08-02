import { Link, NavLink } from "react-router-dom";
import { BrandMark } from "@/components/BrandMark";

const navClass = ({ isActive }: { isActive: boolean }) =>
    `rounded-lg px-3 py-2 text-sm font-medium transition ${isActive
        ? "bg-signal-100 text-signal-600"
        : "text-ink-600 hover:bg-surface-0 hover:text-ink-900"
    }`;

export function Navbar() {
    return (<header className="sticky top-0 z-20 border-b border-surface-2 bg-surface-1/90 backdrop-blur"> <div className="mx-auto flex h-16 max-w-6xl items-center justify-between px-4 sm:px-6"> <Link to="/" className="flex items-center gap-2.5"> <BrandMark className="h-7 w-7" /> <span className="font-display font-semibold text-ink-900">
        BrandDistinct </span> </Link>
        <nav className="flex items-center gap-1">
            <NavLink to="/discover" className={navClass}>
                Discover
            </NavLink>

            <NavLink to="/evaluate" className={navClass}>
                Evaluate
            </NavLink>
        </nav>
    </div>
    </header>


    );
}
