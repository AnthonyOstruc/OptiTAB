# Copilot Instructions for OptiTAB

## Architecture Overview
- **Monorepo** with `backend/` (Django REST API) and `frontend/` (Vue.js + Vite) projects.
- **Backend**: Django 5, REST API, JWT auth, S3 storage, Stripe, Google OAuth, email reset, static/media file management.
- **Frontend**: Vue 3, Vite, Pinia, API calls via `/src/api/`, environment config via `.env` and `VITE_` variables.
- **Deployment**: Render.com (see `render.yaml`), with persistent disk for backend media and S3 for public assets.

## Developer Workflows
### Backend
- Local dev: `cd backend && python manage.py runserver`
- Install deps: `pip install -r requirements.txt`
- Env config: copy `DEV_ENV_SETUP.txt` to `.env` and fill secrets.
- Collect static: `python manage.py collectstatic --noinput`
- Start for production: `./start.sh` (collects static, syncs media, runs Gunicorn)
- Test email reset: configure SMTP/email vars in `.env` or Render secrets.

### Frontend
- Local dev: `cd frontend && npm install && npm run dev`
- Build: `npm run build` (uses Vite)
- Deploy: see `render.yaml` or use `render-build.sh`
- Env config: `.env` with `VITE_API_URL` and `VITE_S3_MEDIA_URL`

## Project Conventions & Patterns
- **Backend apps**: Django apps in `backend/` (e.g. `core/`, `ai/`, `cours/`, `curriculum/`, etc.)
- **API URLs**: Defined per app in `urls.py`, aggregated in `backendAPI/urls.py`.
- **Media/static**: Use S3 for public media, persistent disk for backend media (see `MEDIA_ROOT`).
- **Frontend API**: All API calls in `frontend/src/api/`. Use `VITE_API_URL` for base URL.
- **Course files**: Text files for courses are organized in `frontend/cours/cours_optitab/` by level (e.g. `mpsi/`, `terminal/`).
- **Sensitive config**: Never commit secrets; use `.env` and Render secrets.

## Integration Points
- **Stripe**: `backend/stripe_config.py`, secrets via env vars.
- **S3**: `backend/setup_s3_bucket.py`, Django storages, env vars for keys/bucket.
- **Google OAuth**: Set up in `.env` and Django settings.
- **Email**: SMTP config in `.env` or Render secrets, used for password reset.

## Examples
- Add a new backend API: create a Django app, add to `INSTALLED_APPS`, define `urls.py`, import in `backendAPI/urls.py`.
- Add a new frontend page: create a Vue file in `src/views/`, add route in `src/router/index.js`.

## References
- `backend/DEV_ENV_SETUP.txt` — backend local env setup
- `backend/PRODUCTION_SETUP.md` — production email/password reset
- `frontend/README.md` — frontend dev/build/deploy
- `render.yaml` — Render deployment config

---
For questions or unclear patterns, ask for clarification or check the referenced files.