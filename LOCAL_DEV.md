# Local Dev Environment Setup

This project uses Vite mode-specific environment files so local-only values are never shipped in production builds.

## Env files

- `frontend/.env`
  - Loaded in all modes.
  - Contains only safe shared defaults:
    - `VITE_GTM_ID`
    - `VITE_SITE_URL=https://www.optitab.net`
- `frontend/.env.development`
  - Loaded only for dev mode (`vite`, `npm run dev`).
  - Local API base:
    - `VITE_API_BASE_URL=http://127.0.0.1:8000`
- `frontend/.env.production`
  - Loaded only for production mode (`vite build`).
  - Production API base fallback:
    - `VITE_API_BASE_URL=https://optitab-backend.onrender.com`
  - In CI/deployment, injected env vars (for example via `render.yaml`) can override this value.

## Commands

### Run frontend in development

```bash
npm --prefix frontend run dev
```

### Build frontend for production

```bash
npm --prefix frontend run build
```

### Preview production build locally

```bash
npm --prefix frontend run preview
```

## Quick env checks

### Check resolved development API base URL

```bash
cd frontend
node --input-type=module -e "import { loadEnv } from 'vite'; const env = loadEnv('development', process.cwd(), ''); console.log(env.VITE_API_BASE_URL)"
```

### Check resolved production API base URL

```bash
cd frontend
node --input-type=module -e "import { loadEnv } from 'vite'; const env = loadEnv('production', process.cwd(), ''); console.log(env.VITE_API_BASE_URL)"
```
