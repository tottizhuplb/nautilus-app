from nautilus_trader.adapters.interactive_brokers.config import InteractiveBrokersDataClientConfig
from nautilus_trader.adapters.interactive_brokers.config import InteractiveBrokersInstrumentProviderConfig
from nautilus_trader.adapters.interactive_brokers.factories import InteractiveBrokersLiveDataClientFactory
from nautilus_trader.config import LoggingConfig
from nautilus_trader.config import LiveExecEngineConfig
from nautilus_trader.config import LiveRiskEngineConfig
from nautilus_trader.config import LiveDataEngineConfig
from nautilus_trader.config import LiveStrategiesConfig
from nautilus_trader.config import TraderId
from nautilus_trader.live.node import TradingNode
from nautilus_trader.live.config import TradingNodeConfig

from app.config.ib import (
    IB_HOST,
    IB_PORT,
    IB_CLIENT_ID,
    IB_GATEWAY,
    IB_ACCOUNT_ID,
    MARKET_DATA_TYPE,
    SYMBOLS,
)
from app.strategies.print_ticks import PrintTicksConfig, PrintTicksStrategy


def build_instrument_ids() -> list[str]:
    us = SYMBOLS["US"]
    hk = SYMBOLS["HK"]
    return [
        f"{us['symbol']}.{us['exchange']}",
        f"{hk['symbol']}.{hk['exchange']}",
    ]


def main() -> None:
    instrument_ids = build_instrument_ids()

    data_client_config = InteractiveBrokersDataClientConfig(
        ibg_host=IB_HOST,
        ibg_port=IB_PORT,
        gateway=IB_GATEWAY,
        client_id=IB_CLIENT_ID,
        account_id=IB_ACCOUNT_ID or None,
        market_data_type=MARKET_DATA_TYPE,
        instrument_provider=InteractiveBrokersInstrumentProviderConfig(load_ids=frozenset()),
    )

    strategy = PrintTicksStrategy(
        PrintTicksConfig(
            instrument_ids=instrument_ids,
        )
    )

    node_config = TradingNodeConfig(
        trader_id=TraderId("TRADER-001"),
        logging=LoggingConfig(log_level="INFO"),
        data_engine=LiveDataEngineConfig(),
        risk_engine=LiveRiskEngineConfig(bypass=True),
        exec_engine=LiveExecEngineConfig(reconciliation=False),
        data_clients={
            "IB": data_client_config,
        },
        strategies=LiveStrategiesConfig(strategies=[]),
    )

    node = TradingNode(config=node_config)
    node.add_data_client_factory("IB", InteractiveBrokersLiveDataClientFactory)
    node.trader.add_strategy(strategy)

    try:
        node.build()
        node.run()
    finally:
        node.dispose()


if __name__ == "__main__":
    main()