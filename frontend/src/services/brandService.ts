import { apiPost } from "@/services/apiClient";
import type { DiscoverBrandResult } from "@/types/brand";

interface DiscoverBrandRequest {
  website_url: string;
}

/**
 * POST /api/brand/discover — see 08_api_contracts.md, Endpoint 1.
 * Generates a structured Brand DNA profile from a company website.
 */
export function discoverBrand(websiteUrl: string): Promise<DiscoverBrandResult> {
  return apiPost<DiscoverBrandResult, DiscoverBrandRequest>("/brand/discover", {
    website_url: websiteUrl,
  });
}
