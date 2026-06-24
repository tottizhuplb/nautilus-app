#!/usr/bin/env python3
"""Connectivity smoke checks for compose services."""

from __future__ import annotations

import os
import socket
import sys

import redis

from app.config.env import load_conf_env

load_conf_env()

def check_ib() -> None:
    host = os.getenv("IB_HOST", "ib-gateway")
    port = int(os.getenv("IB_PORT", "4003"))
    with socket.create_connection((host, port), timeout=5):
        print(f"IB gateway reachable at {host}:{port}")


def check_redis() -> None:
    host = os.getenv("REDIS_HOST", "redis")
    port = int(os.getenv("REDIS_PORT", "6379"))
    client = redis.Redis(host=host, port=port, socket_connect_timeout=5)
    if not client.ping():
        raise RuntimeError("Redis ping failed")
    print(f"Redis reachable at {host}:{port}")


def check_nautilus_import() -> None:
    import nautilus_trader  # noqa: F401

    print(f"nautilus_trader import OK ({nautilus_trader.__version__})")


def main() -> int:
    checks = [check_ib, check_redis, check_nautilus_import]
    for check in checks:
        try:
            check()
        except Exception as exc:  # noqa: BLE001 - smoke script
            print(f"FAIL {check.__name__}: {exc}", file=sys.stderr)
            return 1
    print("All smoke checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
