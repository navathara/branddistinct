import { apiPost } from "@/services/apiClient";
import type {
    RewriteRequest,
    RewriteResult,
} from "@/types/rewrite";

export function rewriteContent(
    request: RewriteRequest,
): Promise<RewriteResult> {
    return apiPost<RewriteResult, RewriteRequest>(
        "/rewrite",
        request,
    );
}