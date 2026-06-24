import os

from nautilus_trader.adapters.interactive_brokers.config import IBMarketDataTypeEnum
from nautilus_trader.model.identifiers import InstrumentId

from app.config.env import load_conf_env

load_conf_env()

IB_HOST = os.getenv("IB_HOST", "ib-gateway")
IB_PORT = int(os.getenv("IB_PORT", "4003"))
IB_CLIENT_ID = int(os.getenv("IB_CLIENT_ID", "10"))

_market_data_type = os.getenv("IB_MARKET_DATA_TYPE", "REALTIME").upper()
MARKET_DATA_TYPE = getattr(IBMarketDataTypeEnum, _market_data_type)


def _parse_ticker_list(env_key: str, default: str) -> list[str]:
    raw = os.getenv(env_key, default)
    return [ticker.strip() for ticker in raw.split(",") if ticker.strip()]


US_TICKERS = _parse_ticker_list("US_TICKERS", "AAPL.NASDAQ")
HK_TICKERS = _parse_ticker_list("HK_TICKERS", "700.SEHK")


def build_instrument_ids() -> list[InstrumentId]:
    tickers = US_TICKERS + HK_TICKERS
    return [InstrumentId.from_str(ticker) for ticker in tickers]
