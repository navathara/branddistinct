/// <reference types="vite/client" />

interface ImportMetaEnv {
  /** Base URL for the BrandDistinct AI backend API. Defaults to "/api". */
  readonly VITE_API_BASE_URL?: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
