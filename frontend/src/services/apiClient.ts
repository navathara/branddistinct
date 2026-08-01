import axios, { AxiosError, type AxiosRequestConfig } from "axios";
import type { ApiResponse } from "@/types/api";

/**
 * Base URL for the BrandDistinct AI backend.
 *
 * Falls back to "/api" (the base URL defined in 08_api_contracts.md) so the
 * app works out of the box behind a dev-server proxy or a same-origin
 * deployment. Set VITE_API_BASE_URL to point at a different host.
 */
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "/api";

export const httpClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

/**
 * Thrown by the request helpers below whenever the backend responds with
 * the `{ success: false, error }` envelope, or the request fails before a
 * response is received. Carries the error code from 08_api_contracts.md so
 * calling code can branch on it without re-parsing the response.
 */
export class ApiError extends Error {
  readonly code: string;

  constructor(code: string, message: string) {
    super(message);
    this.name = "ApiError";
    this.code = code;
  }
}

function unwrap<T>(response: ApiResponse<T>): T {
  if (response.success) {
    return response.data;
  }
  throw new ApiError(response.error.code, response.error.message);
}

function toApiError(error: unknown): ApiError {
  if (error instanceof ApiError) return error;

  if (axios.isAxiosError(error)) {
    const axiosError = error as AxiosError<ApiResponse<unknown>>;
    const payload = axiosError.response?.data;
    if (payload && payload.success === false) {
      return new ApiError(payload.error.code, payload.error.message);
    }
    return new ApiError("INTERNAL_ERROR", axiosError.message);
  }

  return new ApiError("INTERNAL_ERROR", "An unexpected error occurred.");
}

/**
 * Generic, envelope-aware GET/POST helpers.
 *
 * These intentionally know nothing about specific endpoints (no
 * `/brand/discover` or `/evaluate` calls live here) — feature modules
 * built on top of this foundation import these helpers and supply their
 * own path and types.
 */
export async function apiGet<T>(
  path: string,
  config?: AxiosRequestConfig,
): Promise<T> {
  try {
    const response = await httpClient.get<ApiResponse<T>>(path, config);
    return unwrap(response.data);
  } catch (error) {
    throw toApiError(error);
  }
}

export async function apiPost<T, Body = unknown>(
  path: string,
  body?: Body,
  config?: AxiosRequestConfig,
): Promise<T> {
  try {
    const response = await httpClient.post<ApiResponse<T>>(path, body, config);
    return unwrap(response.data);
  } catch (error) {
    throw toApiError(error);
  }
}
