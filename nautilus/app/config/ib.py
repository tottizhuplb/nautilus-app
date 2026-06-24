import os

from app.config.env import load_conf_env

load_conf_env()

IB_HOST = os.getenv("IB_HOST", "ib-gateway")
IB_PORT = int(os.getenv("IB_PORT", "4003"))
IB_CLIENT_ID = int(os.getenv("IB_CLIENT_ID", "10"))
IB_GATEWAY = os.getenv("IB_GATEWAY", "true").lower() == "true"
IB_ACCOUNT_ID = os.getenv("TWS_ACCOUNT", "")
MARKET_DATA_TYPE = os.getenv("IB_MARKET_DATA_TYPE", "REALTIME")

SYMBOLS = {
    "US": {
        "symbol": os.getenv("US_SYMBOL", "AAPL"),
        "exchange": os.getenv("US_EXCHANGE", "SMART"),
        "currency": os.getenv("US_CURRENCY", "USD"),
    },
    "HK": {
        "symbol": os.getenv("HK_SYMBOL", "700"),
        "exchange": os.getenv("HK_EXCHANGE", "SEHK"),
        "currency": os.getenv("HK_CURRENCY", "HKD"),
    },
}