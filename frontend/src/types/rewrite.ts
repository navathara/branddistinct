export interface RewriteRequest {
    brand_dna: any;
    content: string;
}

export interface RewriteResult {
    rewritten_content: string;
    improvement_summary: string[];
}