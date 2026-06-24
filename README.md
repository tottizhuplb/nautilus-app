# nautilus-app

Nautilus-centric trading stack with shared Docker Compose base and dev/prod overlays.

## Architecture

```
                ┌───────────────────────┐
                │      nautilus-app     │
                │  live node / backtest │
                │  strategy / actors    │
                └───────────┬───────────┘
                            │
                 ┌──────────┼───────────┐
                 │          │           │
                 ▼          ▼           ▼
          ┌──────────┐ ┌──────────┐ ┌──────────────┐
          │ib-gateway│ │  redis   │ │ parquet data │
          │ 4003/4004│ │   6379   │ │   catalog    │
          └──────────┘ └──────────┘ └──────────────┘
```

- **ib-gateway**: IB login + TWS API (`4003` live / `4004` paper inside compose)
- **redis**: Nautilus cache + optional message-bus backend
- **nautilus/**: live node, backtest, strategies, research

## Quick start

1. Copy env file and fill IB credentials:

```bash
cp .env.example .env
```

2. Start dev stack:

```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d
```

3. Enter the dev container:

```bash
docker exec -it nautilus bash
```

4. Run smoke checks:

```bash
cd /workspace && make smoke
```

5. Run minimal live node (subscribe + log):

```bash
cd /workspace && make live
```

## Production

```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
```

## Dev container

Open this repo in Cursor / VS Code and use **Reopen in Container**. Compose files:

- `docker-compose.yml` (shared base)
- `docker-compose.dev.yml` (dev overlay)

## Layout

```
.
├── docker-compose.yml
├── docker-compose.dev.yml
├── docker-compose.prod.yml
├── .devcontainer/devcontainer.json
├── infra/
│   ├── ib-gateway/notes.md
│   └── redis/data/
└── nautilus/
    ├── Dockerfile.dev
    ├── Dockerfile.prod
    ├── requirements.txt
    ├── Makefile
    ├── conf/
    ├── app/
    │   ├── run_live.py
    │   ├── run_backtest.py
    │   ├── config/
    │   ├── strategies/
    │   ├── actors/
    │   └── research/
    └── data/
        ├── catalog/       # live stream (feather) → convert to parquet
        ├── logs/
        └── checkpoints/
```

## Data on disk

| Location | Role |
|----------|------|
| `infra/redis/data` | Redis AOF (runtime cache / message bus) |
| `nautilus/data/catalog` | Live subscription recordings via `StreamingConfig` |
| `nautilus/data/logs` | App / research logs (reserved) |
| `nautilus/data/checkpoints` | Strategy checkpoints (reserved) |

**Mounts:** dev bind-mounts `./nautilus` → `/workspace` (includes `data/`). Prod bind-mounts `./nautilus/data` → `/app/data` only. Code always uses `nautilus/data/` via `app/config/paths.py`.

After a live run, feather streams land under `catalog/`; use `ParquetDataCatalog.convert_stream_to_data(...)` to materialize parquet for backtest.

## Environment

| File | Purpose |
|------|---------|
| `.env` (repo root) | IB Gateway credentials + `TRADING_MODE` |
| `nautilus/conf/dev.env` | Nautilus settings (loaded at program start) |
| `nautilus/conf/prod.env` | Production nautilus settings |

Compose sets **`NAUTILUS_ENV=dev|prod`** on the nautilus container only. Python loads `conf/{NAUTILUS_ENV}.env` via `app/config/env.py` when you run `run_live`, `smoke`, etc.

| Variable | Where | Purpose |
|----------|-------|---------|
| `NAUTILUS_ENV` | compose overlay | Pick `dev.env` or `prod.env` |
| `TRADING_MODE` | root `.env` | ib-gateway live/paper |
| `IB_PORT` | `conf/*.env` | Nautilus → gateway port |

See [infra/ib-gateway/notes.md](infra/ib-gateway/notes.md) for gateway details.
