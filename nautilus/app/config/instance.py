import os
from pathlib import Path

from nautilus_trader.core.uuid import UUID4

from app.config.env import load_conf_env
from app.config.streaming import CATALOG_PATH

load_conf_env()

_SEQ_FILE = Path(CATALOG_PATH) / ".instance_seq"


def _format_seq_uuid(seq: int) -> str:
    # Valid UUID v4 (version nibble 4, variant RFC 4122) for lexicographic ordering.
    return f"{seq:08x}-0000-4000-8000-{seq:012x}"


def allocate_instance_id() -> UUID4:
    """
    Return the instance ID for this run.

    By default reads/increments a counter under the catalog path so each restart
    gets a new folder that sorts after previous runs (00000001-..., 00000002-...).
    Set STREAMING_INSTANCE_ID to pin a specific UUID v4 for this run.
    """
    override = os.getenv("STREAMING_INSTANCE_ID")
    if override:
        return UUID4.from_str(override.strip())

    _SEQ_FILE.parent.mkdir(parents=True, exist_ok=True)
    seq = int(_SEQ_FILE.read_text().strip()) if _SEQ_FILE.exists() else 0
    seq += 1
    _SEQ_FILE.write_text(str(seq))
    return UUID4.from_str(_format_seq_uuid(seq))
