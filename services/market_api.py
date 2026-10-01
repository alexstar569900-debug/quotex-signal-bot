import requests
from config.settings import API_BASE_URL


class MarketAPI:
    def __init__(self, base_url=API_BASE_URL):
        self.base_url = base_url

    def get_klines(self, symbol: str, interval: str = "1h", limit: int = 200):
        url = f"{self.base_url}/klines"
        params = {
            "symbol": symbol.upper(),
            "interval": interval,
            "limit": limit,
        }
        response = requests.get(url, params=params, timeout=20)
        response.raise_for_status()
        return response.json()

    def get_candle_dataframe(self, symbol: str, interval: str = "1h", limit: int = 200):
        raw = self.get_klines(symbol=symbol, interval=interval, limit=limit)
        rows = []
        for item in raw:
            rows.append({
                "open_time": item[0],
                "open": float(item[1]),
                "high": float(item[2]),
                "low": float(item[3]),
                "close": float(item[4]),
                "volume": float(item[5]),
                "close_time": item[6],
            })
        import pandas as pd
        df = pd.DataFrame(rows)
        return df
