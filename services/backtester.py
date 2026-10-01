import pandas as pd


def backtest_strategy(df: pd.DataFrame, initial_capital: float = 1000.0):
    data = df.copy().reset_index(drop=True)
    if "close" not in data.columns:
        raise ValueError("DataFrame must contain 'close' column")

    data["ema_fast"] = data["close"].ewm(span=9, adjust=False).mean()
    data["ema_slow"] = data["close"].ewm(span=21, adjust=False).mean()
    data["rsi"] = data["close"].pct_change().fillna(0)

    position = 0
    cash = initial_capital
    trade_count = 0
    wins = 0
    losses = 0
    equity_curve = []
    entry_price = 0.0

    for i in range(1, len(data)):
        prev = data.iloc[i - 1]
        curr = data.iloc[i]

        signal = None
        if curr["ema_fast"] > curr["ema_slow"] and prev["ema_fast"] <= prev["ema_slow"]:
            signal = "BUY"
        elif curr["ema_fast"] < curr["ema_slow"] and prev["ema_fast"] >= prev["ema_slow"]:
            signal = "SELL"

        if signal == "BUY" and position == 0:
            position = 1
            entry_price = curr["close"]
        elif signal == "SELL" and position == 1:
            pnl = (curr["close"] - entry_price) / entry_price
            cash = cash * (1 + pnl)
            trade_count += 1
            if pnl > 0:
                wins += 1
            else:
                losses += 1
            position = 0
            entry_price = 0.0

        equity_curve.append(cash if position == 0 else cash + (curr["close"] * position))

    final_balance = cash if position == 0 else cash + (data.iloc[-1]["close"] * position)

    result = {
        "initial_capital": initial_capital,
        "final_balance": final_balance,
        "profit": final_balance - initial_capital,
        "trades": trade_count,
        "wins": wins,
        "losses": losses,
        "win_rate": (wins / trade_count) if trade_count else 0,
    }
    return result

