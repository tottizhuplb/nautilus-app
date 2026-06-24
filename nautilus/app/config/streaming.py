import os

from nautilus_trader.config import StreamingConfig
from nautilus_trader.model.data import QuoteTick
from nautilus_trader.model.data import TradeTick
from nautilus_trader.persistence.writer import RotationMode

from app.config.env import load_conf_env

load_conf_env()

CATALOG_PATH = os.getenv("DATA_CATALOG_PATH", "data/catalog")
FLUSH_INTERVAL_MS = int(os.getenv("STREAMING_FLUSH_INTERVAL_MS", "1000"))


def build_streaming_config() -> StreamingConfig:
    return StreamingConfig(
        catalog_path=CATALOG_PATH,
        flush_interval_ms=FLUSH_INTERVAL_MS,
        include_types=[QuoteTick, TradeTick],
        rotation_mode=RotationMode.SCHEDULED_DATES,
        rotation_timezone="UTC",
    )
