# Frontend

The frontend is a minimal Vue 3 + Vite application for browsing events produced by the simulator and stored by the backend.

## Implemented Scope

- event list view
- simple filters for `severity` and `service_name`
- lightweight event detail panel
- event summary cards
- periodic refresh
- clean, minimal UI

## Environment Variables

- `VITE_API_BASE_URL`
- `VITE_POLL_INTERVAL_MS`

Example local configuration:

```env
VITE_API_BASE_URL=http://localhost:8000
VITE_POLL_INTERVAL_MS=10000
```

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
