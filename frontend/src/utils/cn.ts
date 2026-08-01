export type ClassValue = string | number | null | undefined | false;

/**
 * Joins truthy class name values with a single space, skipping
 * `null`/`undefined`/`false`/empty-string entries.
 *
 * Usage: `cn("base", isActive && "active", className)`
 */
export function cn(...values: ClassValue[]): string {
  return values.filter(Boolean).join(" ");
}
