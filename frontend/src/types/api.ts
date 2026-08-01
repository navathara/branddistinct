/**
 * Shared API envelope types.
 *
 * Mirrors the "Standard Response Format" and "Error Codes" table defined in
 * 08_api_contracts.md. Every backend endpoint returns one of these two
 * shapes, so the API client and future feature modules can rely on a single
 * pair of types instead of re-declaring response shapes per endpoint.
 */

/** Error codes from the API Contracts "Error Codes" table. */
export type ApiErrorCode =
  | "INVALID_URL"
  | "WEBSITE_UNREACHABLE"
  | "INSUFFICIENT_BRAND_DATA"
  | "INVALID_CONTENT"
  | "INVALID_REQUEST"
  | "AI_RESPONSE_ERROR"
  | "INTERNAL_ERROR";

export interface ApiSuccessResponse<T> {
  success: true;
  data: T;
  message?: string;
}

export interface ApiErrorResponse {
  success: false;
  error: {
    code: ApiErrorCode;
    message: string;
  };
}

export type ApiResponse<T> = ApiSuccessResponse<T> | ApiErrorResponse;
