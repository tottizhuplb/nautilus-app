from nautilus_trader.adapters.interactive_brokers.common import IB
from nautilus_trader.adapters.interactive_brokers.config import InteractiveBrokersDataClientConfig
from nautilus_trader.adapters.interactive_brokers.config import InteractiveBrokersInstrumentProviderConfig
from nautilus_trader.adapters.interactive_brokers.factories import InteractiveBrokersLiveDataClientFactory
from nautilus_trader.config import LoggingConfig
from nautilus_trader.config import LiveDataEngineConfig
from nautilus_trader.config import LiveExecEngineConfig
from nautilus_trader.config import LiveRiskEngineConfig
from nautilus_trader.config import TradingNodeConfig
from nautilus_trader.live.node import TradingNode
from nautilus_trader.model.identifiers import TraderId

from app.config.ib import IB_CLIENT_ID
from app.config.ib import IB_HOST
from app.config.ib import IB_PORT
from app.config.ib import MARKET_DATA_TYPE
from app.config.ib import build_instrument_ids
from app.config.instance import allocate_instance_id
from app.config.streaming import build_streaming_config
from app.strategies.print_ticks import PrintTicksConfig
from app.strategies.print_ticks import PrintTicksStrategy


def main() -> None:
    instrument_ids = build_instrument_ids()

    data_client_config = InteractiveBrokersDataClientConfig(
        ibg_host=IB_HOST,
        ibg_port=IB_PORT,
        ibg_client_id=IB_CLIENT_ID,
        use_regular_trading_hours=True,
        market_data_type=MARKET_DATA_TYPE,
        instrument_provider=InteractiveBrokersInstrumentProviderConfig(
            load_ids=frozenset(instrument_ids),
        ),
    )

    strategy = PrintTicksStrategy(
        PrintTicksConfig(
            instrument_ids=instrument_ids,
        ),
    )

    node_config = TradingNodeConfig(
        trader_id=TraderId("TRADER-001"),
        instance_id=allocate_instance_id(),
        logging=LoggingConfig(log_level="INFO"),
        data_engine=LiveDataEngineConfig(
            time_bars_timestamp_on_close=False,
            validate_data_sequence=True,
        ),
        risk_engine=LiveRiskEngineConfig(bypass=True),
        exec_engine=LiveExecEngineConfig(reconciliation=False),
        data_clients={IB: data_client_config},
        streaming=build_streaming_config(),
        timeout_connection=90.0,
    )

    node = TradingNode(config=node_config)
    node.add_data_client_factory(IB, InteractiveBrokersLiveDataClientFactory)
    node.trader.add_strategy(strategy)

    try:
        node.build()
        node.run()
    finally:
        node.dispose()


if __name__ == "__main__":
    main()
