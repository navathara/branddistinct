/**
 * Brand DNA domain types.
 *
 * The backend's Brand Discovery Engine extracts these from a website and
 * returns them under `data.brand_dna` from `POST /api/brand/discover`
 * (see 08_api_contracts.md). Field values are AI-extracted free text /
 * lists, so each dimension is typed as a loose record — the six
 * *dimension keys* are the contract; the shape of what's inside each one
 * is deliberately flexible so the UI can render whatever the backend
 * actually fills in without falling over on a schema mismatch.
 */
export type BrandDnaFieldValue =
  | string
  | string[]
  | number
  | boolean
  | null
  | undefined;

export type BrandDnaDimension = Record<string, BrandDnaFieldValue>;

/** The six canonical dimensions from 01_brand_dna.yaml's evaluation_reference. */
export interface BrandDna {
  identity: BrandDnaDimension;
  personality: BrandDnaDimension;
  communication: BrandDnaDimension;
  audience: BrandDnaDimension;
  visual_identity: BrandDnaDimension;
  values: BrandDnaDimension;
}

export const BRAND_DNA_DIMENSION_KEYS = [
  "identity",
  "personality",
  "communication",
  "audience",
  "visual_identity",
  "values",
] as const;

/** Human-readable labels for each dimension, used in the UI. */
export const BRAND_DNA_DIMENSION_LABELS: Record<keyof BrandDna, string> = {
  identity: "Identity",
  personality: "Personality",
  communication: "Communication",
  audience: "Audience",
  visual_identity: "Visual Identity",
  values: "Values",
};

/** `data` shape of a successful POST /api/brand/discover response. */
export interface DiscoverBrandResult {
  brand_id: string;
  brand_name: string;
  brand_dna: BrandDna;
  extraction_confidence: number;
}
