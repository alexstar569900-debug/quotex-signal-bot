import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator


class SignalEngine:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    def prepare(self):
        if "close" not in self.df.columns:
            raise ValueError("DataFrame must contain 'close' column")

        self.df["close"] = pd.to_numeric(self.df["close"], errors="coerce")
        self.df = self.df.dropna(subset=["close"]).reset_index(drop=True)

        self.df["ema_fast"] = EMAIndicator(close=self.df["close"], window=9).ema_indicator()
        self.df["ema_slow"] = EMAIndicator(close=self.df["close"], window=21).ema_indicator()
        self.df["rsi"] = RSIIndicator(close=self.df["close"], window=14).rsi()
        return self.df

    def generate_signal(self):
        data = self.prepare()
        if len(data) < 2:
            return {"signal": "HOLD", "reason": "Not enough data"}

        latest = data.iloc[-1]
        previous = data.iloc[-2]

        bullish = (
            latest["ema_fast"] > latest["ema_slow"]
            and previous["ema_fast"] <= previous["ema_slow"]
            and latest["rsi"] > 50
        )

        bearish = (
            latest["ema_fast"] < latest["ema_slow"]
            and previous["ema_fast"] >= previous["ema_slow"]
            and latest["rsi"] < 50
        )

        if bullish:
            return {"signal": "BUY", "reason": "EMA bullish crossover and RSI above 50"}
        elif bearish:
            return {"signal": "SELL", "reason": "EMA bearish crossover and RSI below 50"}
        else:
            return {"signal": "HOLD", "reason": "No strong signal"}
