import pandas as pd
from fastapi import FastAPI
from services.market_api import MarketAPI
from services.signal_engine import SignalEngine
from services.backtester import backtest_strategy

app = FastAPI(title="Signal Bot Demo")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/signal")
def get_signal(symbol: str = "BTCUSDT", interval: str = "1h", limit: int = 200):
    api = MarketAPI()
    df = api.get_candle_dataframe(symbol=symbol, interval=interval, limit=limit)
    if df.empty:
        return {"signal": "HOLD", "reason": "No data returned"}

    engine = SignalEngine(df)
    result = engine.generate_signal()
    return {
        "symbol": symbol,
        "interval": interval,
        "signal": result["signal"],
        "reason": result["reason"],
    }


@app.get("/backtest")
def run_backtest(symbol: str = "BTCUSDT", interval: str = "1h", limit: int = 500):
    api = MarketAPI()
    df = api.get_candle_dataframe(symbol=symbol, interval=interval, limit=limit)
    if df.empty:
        return {"error": "No data returned"}

    metrics = backtest_strategy(df)
    return {
        "symbol": symbol,
        "interval": interval,
        "metrics": metrics,
    }
