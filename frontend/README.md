# BrandDistinct AI — Frontend

React + TypeScript + Vite + Tailwind CSS + Axios.

This is the **frontend foundation only**. Brand Discovery, Content
Evaluation, and the Results Dashboard are separate milestones built on top
of this scaffold — see `07_developer_handbook.md` and
`08_api_contracts.md` for the specs they must follow.

## Getting started

```bash
npm install
cp .env.example .env   # point VITE_API_BASE_URL at the backend
npm run dev
```

Other scripts: `npm run build` (type-check + production build),
`npm run preview` (serve the build locally), `npm run lint` (oxlint).

## Structure

```
src/
  components/   Shared, reusable UI (Navbar, Footer, Layout, BrandMark, ...)
  pages/        Route-level components (Home, NotFound)
  services/     Axios instance + generic, envelope-aware request helpers
  hooks/        Reusable React hooks (e.g. useApi)
  types/        Shared TypeScript types (API envelope, error codes)
  utils/        Small framework-agnostic helpers (e.g. cn)
  App.tsx       Route table
  main.tsx      Entry point (BrowserRouter + App)
```

## Conventions

- **Folder responsibilities mirror the backend handbook**: `services/`
  only talks to the API, `pages/` compose `components/`, and business
  logic for a given feature lives with that feature — none of it belongs
  in this foundation layer.
- **API client**: `services/apiClient.ts` exports `apiGet`/`apiPost`,
  which unwrap the `{ success, data }` / `{ success, error }` envelope
  from `08_api_contracts.md` and throw a typed `ApiError` on failure.
  It does not hardcode any endpoint paths — feature modules built later
  (Brand Discovery, Evaluation) own their own request functions.
- **Styling**: Tailwind v4, configured via `@theme` tokens in
  `src/index.css` rather than a `tailwind.config.js`. Colors, fonts, and
  radii are all named tokens (`surface-*`, `ink-*`, `signal-*`,
  `font-display`, etc.) so future pages stay visually consistent.
- **Routing**: `/` renders `Home`. `/discover` is reserved for the future
  Brand Discovery page and currently falls through to the generic
  `NotFound` route — it is intentionally not implemented here.
