from nautilus_trader.trading.strategy import Strategy
from nautilus_trader.trading.strategy import StrategyConfig


class PrintTicksConfig(StrategyConfig, frozen=True):
    instrument_ids: list[str]


class PrintTicksStrategy(Strategy):
    def __init__(self, config: PrintTicksConfig):
        super().__init__(config)

    def on_start(self) -> None:
        self.log.info("PrintTicksStrategy starting")
        for instrument_id in self.config.instrument_ids:
            self.log.info(f"Subscribing to {instrument_id}")
            self.subscribe_quote_ticks(instrument_id)
            self.subscribe_trade_ticks(instrument_id)

    def on_quote_tick(self, tick) -> None:
        self.log.info(
            f"QUOTE {tick.instrument_id} bid={tick.bid_price} x {tick.bid_size} | ask={tick.ask_price} x {tick.ask_size} ts={tick.ts_event}"
        )

    def on_trade_tick(self, tick) -> None:
        self.log.info(
            f"TRADE {tick.instrument_id} price={tick.price} size={tick.size} aggressor={tick.aggressor_side} ts={tick.ts_event}"
        )