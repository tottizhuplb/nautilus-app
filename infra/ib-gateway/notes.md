# IB Gateway (dockerized)

This stack uses [gnzsnz/ib-gateway](https://github.com/gnzsnz/ib-gateway-docker) as the TWS API endpoint.

## Ports

| Mode  | Container port | Host bind   |
|-------|----------------|-------------|
| live  | 4003           | 127.0.0.1   |
| paper | 4004           | 127.0.0.1   |
| VNC   | 5900           | 127.0.0.1   |

Nautilus connects to `ib-gateway:4003` (live) or `ib-gateway:4004` (paper) from inside the compose network.

## Credentials

Set in root `.env`:

- `IBKR_USERID`
- `IBKR_PASSWORD`
- `VNC_SERVER_PASSWORD`

## Gateway defaults

Fixed in `docker-compose.yml` (edit there if you need to change 2FA/restart/timezone behaviour). Only `TRADING_MODE` is also read from `.env` (use `paper` + `IB_PORT=4004` for paper).

## TWS settings persistence

Gateway config is bind-mounted from the repo:

```
infra/ib-gateway/tws_settings  →  /home/ibgateway/tws_settings
```

Contents are gitignored (session/state); only the directory is tracked.

## Debugging

- VNC: `127.0.0.1:5900`, password from `VNC_SERVER_PASSWORD`
- Healthcheck uses `pgrep` for socat `TCP-LISTEN` on the mode port — not a TCP connect (that would trigger Gateway "disconnected before version was sent")
- First login can take 1–2 minutes; healthcheck `start_period` is 120s

## Notes

Official Nautilus docs reference IB Gateway ports 4001/4002 for native installs. The dockerized wrapper maps to 4003/4004 — set `IB_PORT` accordingly.
