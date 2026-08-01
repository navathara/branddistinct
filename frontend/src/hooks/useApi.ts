import { useCallback, useState } from "react";
import { ApiError } from "@/services/apiClient";

type ApiState<T> =
  | { status: "idle"; data: null; error: null }
  | { status: "loading"; data: null; error: null }
  | { status: "success"; data: T; error: null }
  | { status: "error"; data: null; error: ApiError };

/**
 * Wraps an async call (typically one built on `apiGet`/`apiPost`) and
 * exposes its status, data, and error as state, plus a `run` function to
 * trigger it.
 *
 * This hook is intentionally generic — it knows nothing about brand
 * discovery or evaluation specifically. Feature pages call it with their
 * own request function, e.g.:
 *
 *   const { status, data, error, run } = useApi(discoverBrand);
 *   run({ website_url: url });
 */
export function useApi<TArgs extends unknown[], TResult>(
  requestFn: (...args: TArgs) => Promise<TResult>,
) {
  const [state, setState] = useState<ApiState<TResult>>({
    status: "idle",
    data: null,
    error: null,
  });

  const run = useCallback(
    async (...args: TArgs) => {
      setState({ status: "loading", data: null, error: null });
      try {
        const data = await requestFn(...args);
        setState({ status: "success", data, error: null });
        return data;
      } catch (error) {
        const apiError =
          error instanceof ApiError
            ? error
            : new ApiError("INTERNAL_ERROR", "An unexpected error occurred.");
        setState({ status: "error", data: null, error: apiError });
        throw apiError;
      }
    },
    [requestFn],
  );

  const reset = useCallback(() => {
    setState({ status: "idle", data: null, error: null });
  }, []);

  return { ...state, run, reset };
}
