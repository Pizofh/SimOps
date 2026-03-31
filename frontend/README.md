# Frontend

The frontend is a minimal Vue 3 + Vite application for browsing events produced by the simulator and stored by the backend.

## Implemented Scope

- event list view
- simple filters for `severity` and `service_name`
- detail panel backed by `GET /events/{id}`
- summary cards
- periodic refresh
- clean, minimal UI

## Environment Variables

For local Vite development:

- `VITE_API_BASE_URL`
- `VITE_POLL_INTERVAL_MS`

Example:

```env
VITE_API_BASE_URL=http://localhost:8000
VITE_POLL_INTERVAL_MS=10000
```

For the containerized frontend:

- `SIMOPS_API_BASE_URL`

This variable is injected at container startup into a runtime `config.js`, which means the frontend image does not need to be rebuilt every time the API endpoint changes.

## Run Locally

Run from the `frontend/` directory.

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

Build for production:

```bash
npm run build
```

Lint:

```bash
npm run lint
```

## Run in Docker Compose

From the repository root:

```bash
docker compose up --build frontend
```

The frontend is served by Nginx on port `8080` by default.

