### Monorepo: Frontend + Backend + Postgres (Single Hostname)

This repo runs the frontend, FastAPI backend, and PostgreSQL behind a single reverse proxy.

#### Repository Structure

```
root/
├─ frontend/                     # Vite React frontend
├─ backend/                      # FastAPI + PostgreSQL
├─ infra/
│  └─ nginx/                     # Reverse proxy
├─ docker-compose.yml
└─ README.md
```

#### Routing (Single Hostname)

- `/` → frontend
- `/api` → backend
- `/docs` → backend Swagger UI
- `/openapi.json` → backend OpenAPI schema

#### Local Run (Docker Compose)

1) Build and run:

```bash
docker compose up --build
```

#### Backend Endpoints
- `GET /api/health/period?project_name=...`
- `GET /api/settings/health-polling?project_name=...`
- `PUT /api/settings/health-polling`
- `POST /api/health/results/truncate`

## DB 탐색 및 삭제 커맨드 (external URL)

테이블 목록:

```bash
psql "postgresql://console:KXYxjRTEVu8sCDV4Vu35QrUCoMfkHD6v@dpg-d574sjemcj7s7388i9i0-a.singapore-postgres.render.com:5432/appdb_dqo3" -c "\dt"
```

health_settings 조회:

```bash
psql "postgresql://console:KXYxjRTEVu8sCDV4Vu35QrUCoMfkHD6v@dpg-d574sjemcj7s7388i9i0-a.singapore-postgres.render.com:5432/appdb_dqo3" -c "SELECT * FROM health_settings ORDER BY updated_at DESC;"
```

health_results 조회:

```bash
psql "postgresql://console:KXYxjRTEVu8sCDV4Vu35QrUCoMfkHD6v@dpg-d574sjemcj7s7388i9i0-a.singapore-postgres.render.com:5432/appdb_dqo3" -c "SELECT * FROM health_results ORDER BY created_at DESC"
```

health_results 삭제 (프로젝트별):

```bash
psql "postgresql://console:KXYxjRTEVu8sCDV4Vu35QrUCoMfkHD6v@dpg-d574sjemcj7s7388i9i0-a.singapore-postgres.render.com:5432/appdb_dqo3" -c "DELETE FROM health_results WHERE project_name='paper-service';"
```

health_results 전체 초기화:

```bash
psql "postgresql://console:KXYxjRTEVu8sCDV4Vu35QrUCoMfkHD6v@dpg-d574sjemcj7s7388i9i0-a.singapore-postgres.render.com:5432/appdb_dqo3" -c "TRUNCATE TABLE health_results RESTART IDENTITY;"
```

## Frontend API Base

The frontend calls the backend via `/api`. For local development without Docker:

```bash
cd frontend
npm install
npm run dev
```

The Vite dev server proxies `/api` to `http://localhost:8000` via `vite.config.ts`.

## Deployment (Server)

1) Clone repo
2) Create `.env`
3) Run:

```bash
docker compose up -d --build
```

Postgres data is persisted in a Docker volume (`postgres_data`).
