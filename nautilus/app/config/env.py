import os
from pathlib import Path

from dotenv import load_dotenv

_CONF_DIR = Path(__file__).resolve().parents[2] / "conf"


def load_conf_env() -> None:
    name = os.getenv("NAUTILUS_ENV", "dev")
    load_dotenv(_CONF_DIR / f"{name}.env", override=False)
