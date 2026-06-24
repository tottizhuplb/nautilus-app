from typing import Any

from nautilus_trader.model.identifiers import ClientId, InstrumentId
from nautilus_trader.trading.config import StrategyConfig

class Strategy:
    config: StrategyConfig
    log: Any

    def __init__(self, config: StrategyConfig | None = None) -> None: ...
    def on_start(self) -> None: ...
    def on_stop(self) -> None: ...
    def on_quote_tick(self, tick: Any) -> None: ...
    def on_trade_tick(self, tick: Any) -> None: ...
    def subscribe_quote_ticks(
        self,
        instrument_id: InstrumentId,
        client_id: ClientId | None = None,
        update_catalog: bool = False,
        aggregate_spread_quotes: bool = False,
        params: dict[str, object] | None = None,
    ) -> None: ...
    def subscribe_trade_ticks(
        self,
        instrument_id: InstrumentId,
        client_id: ClientId | None = None,
        update_catalog: bool = False,
        params: dict[str, object] | None = None,
    ) -> None: ...
